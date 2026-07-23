"use client";

import { useState } from "react";
import { Message, SourceChunk } from "@/types/chat";



export function useChatStream() {


    const [messages, setMessages] = useState<Message[]>([])
    const [conversationId, setConversationId] = useState<string | null>(null)
    const [isStreaming, setIsStreaming] = useState(false)

    const sendMessage = async (question: string) => {
        if (!question.trim() || isStreaming) return

        const userMessage: Message = {
            id: crypto.randomUUID(),
            role: "user",
            content: question

        }
        const assistantMsgId = crypto.randomUUID()
        const asisstantMessage: Message = {
            id: assistantMsgId,
            role: "assistant",
            content: ""

        }


        setMessages((prev) => [...prev, userMessage, asisstantMessage])
        setIsStreaming(true)

        try {
            const response = await fetch("http://localhost:8000/chat/", {
                method: "post",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question,
                    conversation_id: conversationId
                }
                )
            }
            )

            if (!response.ok || !response.body) {
                throw new Error("Failed to fetch the api response")
            }


            const reader = response.body.getReader()
            const decoder = new TextDecoder()
            let done = false
            let buffer = ""

            while (!done) {
                const { value, done: readerDone } = await reader.read()
                done = readerDone
                if (value) {
                    buffer += decoder.decode(value, { stream: true })

                    const lines = buffer.split("\n\n")
                    buffer = lines.pop() || ""

                    for (const line of lines) {

                        const trimmedLine = line.trim()
                        if (!trimmedLine.startsWith("data: ")) continue

                        const dataString = trimmedLine.replace("data: ", "").trim()

                        if (dataString === "[DONE]") {
                            done = true
                            break
                        }
                        try {
                            const parsed = JSON.parse(dataString)
                            if (parsed.source) {
                                setMessages((prev) =>
                                    prev.map((msg) =>
                                        msg.id === assistantMsgId
                                            ? { ...msg, sources: parsed.source }
                                            : msg
                                    )
                                );
                            }

                            if (parsed.answer_chunk) {
                                setMessages((prev) =>
                                    prev.map((msg) =>
                                        msg.id === assistantMsgId
                                            ? { ...msg, content: msg.content + parsed.answer_chunk }
                                            : msg
                                    )
                                );
                            }

                            if (parsed.answer) {
                                setMessages((prev) =>
                                    prev.map((msg) =>
                                        msg.id === assistantMsgId
                                            ? { ...msg, content: parsed.answer, sources: parsed.source || [] }
                                            : msg
                                    )
                                );
                            }

                        } catch (err) {
                            console.error("Failed to parse SSE JSON chunk:", dataString, err);
                        }
                    }
                }
            }
        } catch (error) {
            console.error("Stream connection error:", error);
            setMessages((prev) =>
                prev.map((msg) =>
                    msg.id === assistantMsgId
                        ? { ...msg, content: "Connection error occurred while generating response." }
                        : msg
                )
            );
        } finally {
            setIsStreaming(false);
        }
    };

    const submitFeedback = async (messageId: string, rating: "thumbs_up" | "thumbs_down") => {
        try {

            setMessages((prev) =>
                prev.map((msg) =>
                    msg.id === messageId ? { ...msg, feedback: rating } : msg
                )
            );

            const response = await fetch("http://localhost:8000/chat/feedback", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message_id: messageId,
                    rating: rating,
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to submit feedback");
            }
        } catch (error) {
            console.error("Error sending feedback:", error);
        }
    };




    return {
        messages,
        conversationId,
        isStreaming,
        sendMessage,
        submitFeedback
    };
}




