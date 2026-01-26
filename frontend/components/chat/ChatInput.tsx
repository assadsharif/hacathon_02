/**
 * ChatInput Component
 * [Task]: C1 - ChatKit UI component
 * [Refs]: specs/phase-iii/plan.md#file-structure
 *
 * Text input for sending messages to the TodoAgent.
 */

'use client';

import { useState, useRef, useEffect, KeyboardEvent } from 'react';

interface ChatInputProps {
  /** Called when user submits a message */
  onSend: (message: string) => void;
  /** Disable input (e.g., while processing) */
  disabled?: boolean;
  /** Placeholder text */
  placeholder?: string;
}

/**
 * Chat input component with send button.
 * Supports Enter to send and Shift+Enter for new lines.
 */
export function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Type a message...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
    }
  }, [message]);

  const handleSubmit = () => {
    const trimmed = message.trim();
    if (trimmed && !disabled) {
      onSend(trimmed);
      setMessage('');
      // Reset height after clearing
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'flex-end',
        gap: '12px',
        padding: '16px',
        borderTop: '1px solid #e5e7eb',
        backgroundColor: '#ffffff',
      }}
    >
      <textarea
        ref={textareaRef}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        rows={1}
        style={{
          flex: 1,
          padding: '12px 16px',
          borderRadius: '20px',
          border: '1px solid #e5e7eb',
          backgroundColor: disabled ? '#f3f4f6' : '#f3f4f6',
          fontSize: '15px',
          lineHeight: '1.4',
          resize: 'none',
          outline: 'none',
          fontFamily: 'inherit',
          minHeight: '44px',
          maxHeight: '150px',
          color: disabled ? '#9ca3af' : '#1f2937',
        }}
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || !message.trim()}
        style={{
          padding: '12px 20px',
          borderRadius: '20px',
          border: 'none',
          backgroundColor:
            disabled || !message.trim() ? '#e5e7eb' : '#8b5cf6',
          color: disabled || !message.trim() ? '#9ca3af' : '#ffffff',
          fontSize: '15px',
          fontWeight: '600',
          cursor: disabled || !message.trim() ? 'not-allowed' : 'pointer',
          transition: 'background-color 0.2s',
          whiteSpace: 'nowrap',
        }}
      >
        Send
      </button>
    </div>
  );
}

export default ChatInput;
