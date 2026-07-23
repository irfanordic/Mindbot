
export interface SourceChunk {
    chunk_index: number,
    chunk_content: string,
    distance: number
}


export interface Message {
    id: string
    role: 'user' | 'assistant'
    content: string
    sources?: SourceChunk[]
    feedback?: 'thumbs_up' | 'thumbs_down' | null
}

export interface ChatPayload {
    question: string;
    conversation_id: string | null;
}