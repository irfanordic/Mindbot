"use client";

import { useState } from "react";
import { useChatStream } from "../hooks/useChatStream";

export default function ChatPage() {
  const [input, setInput] = useState("");
  // Pull submitFeedback from our hook
  const { messages, isStreaming, sendMessage, submitFeedback } = useChatStream();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <header className="py-4 border-b border-gray-200 dark:border-gray-800 mb-4">
        <h1 className="text-2xl font-bold text-center">🤖 MindBot RAG Assistant</h1>
      </header>

      <div className="flex-1 overflow-y-auto space-y-4 p-4 rounded-lg bg-white dark:bg-gray-800 shadow-inner">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            Ask a question about your documents to start chatting!
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"
                }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                  }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>

                {/* Sources Display */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-gray-300 dark:border-gray-600 text-xs">
                    <p className="font-semibold mb-1">📚 Sources used:</p>
                    <ul className="list-disc list-inside space-y-1 opacity-80">
                      {msg.sources.map((src, idx) => (
                        <li key={idx}>
                          Chunk #{src.chunk_index} (Distance: {src.distance})
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* ────── FEEDBACK BUTTONS (ONLY FOR ASSISTANT MESSAGES) ────── */}
              {msg.role === "assistant" && msg.content && (
                <div className="flex items-center gap-2 mt-1 px-2 text-xs text-gray-500">
                  <span>Feedback:</span>
                  <button
                    onClick={() => submitFeedback(msg.id, "thumbs_up")}
                    className={`hover:text-green-500 transition-colors ${msg.feedback === "thumbs_up" ? "text-green-500 font-bold" : ""
                      }`}
                  >
                    👍
                  </button>
                  <button
                    onClick={() => submitFeedback(msg.id, "thumbs_down")}
                    className={`hover:text-red-500 transition-colors ${msg.feedback === "thumbs_down" ? "text-red-500 font-bold" : ""
                      }`}
                  >
                    👎
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          disabled={isStreaming}
          className="flex-1 px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={isStreaming || !input.trim()}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl disabled:opacity-50 transition-colors"
        >
          {isStreaming ? "Thinking..." : "Send"}
        </button>
      </form>
    </div>
  );
}