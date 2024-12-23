"use client";

import { useChat } from "ai/react";

export default function Chat() {
  const httpUrl = `${process.env.NEXT_PUBLIC_BACKEND_HTTP_PROTOCOL}://${process.env.NEXT_PUBLIC_BACKEND_HOST}`;
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: `${httpUrl}/api/chat`,
    streamProtocol: "text",
  });

  return (
    <div className="flex flex-col w-full max-w-md py-6 mx-auto stretch">
      {messages.map((m) => (
        <div key={m.id} className="whitespace-pre-wrap">
          {m.role === "user" ? "You: " : "Donny: "}
          {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input
          className="w-full max-w-md p-2 my-6 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}
