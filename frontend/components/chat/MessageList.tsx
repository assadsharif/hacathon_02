/**
 * MessageList Component
 * [Task]: C1, C3 - ChatKit UI component with tool invocation display
 * [Refs]: specs/phase-iii/plan.md#file-structure, tasks.md#c3
 *
 * Displays chat messages with support for:
 * - User messages
 * - Assistant responses
 * - Tool invocation visibility (toggleable)
 */

'use client';

import { useRef, useEffect, useState } from 'react';

/**
 * Tool call information for display
 */
export interface ToolCallDisplay {
  name: string;
  args: unknown;
  result?: {
    success: boolean;
    data?: unknown;
    error?: string;
  };
}

/**
 * Chat message structure
 */
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  /** Tool calls made during this message (assistant only) */
  toolCalls?: ToolCallDisplay[];
  /** Is the message still being processed */
  isLoading?: boolean;
}

interface MessageListProps {
  /** Messages to display */
  messages: ChatMessage[];
  /** Show/hide tool invocations */
  showToolCalls?: boolean;
}

/**
 * Format a tool call for display
 */
function formatToolArgs(args: unknown): string {
  try {
    return JSON.stringify(args, null, 2);
  } catch {
    return String(args);
  }
}

/**
 * Single message component
 */
function Message({
  message,
  showToolCalls,
}: {
  message: ChatMessage;
  showToolCalls: boolean;
}) {
  const [expandedTools, setExpandedTools] = useState<Set<number>>(new Set());

  const toggleTool = (index: number) => {
    const newExpanded = new Set(expandedTools);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedTools(newExpanded);
  };

  const isUser = message.role === 'user';

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: isUser ? 'flex-end' : 'flex-start',
        marginBottom: '16px',
      }}
    >
      {/* Message bubble */}
      <div
        style={{
          maxWidth: '80%',
          padding: '12px 16px',
          borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
          backgroundColor: isUser ? '#3b82f6' : '#8b5cf6',
          color: '#ffffff',
          fontSize: '15px',
          lineHeight: '1.4',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}
      >
        {message.isLoading ? (
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span
              style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: '#ffffff',
                animation: 'pulse 1.4s ease-in-out infinite',
              }}
            />
            <span
              style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: '#ffffff',
                animation: 'pulse 1.4s ease-in-out 0.2s infinite',
              }}
            />
            <span
              style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: '#ffffff',
                animation: 'pulse 1.4s ease-in-out 0.4s infinite',
              }}
            />
            <style>{`
              @keyframes pulse {
                0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
                40% { transform: scale(1); opacity: 1; }
              }
            `}</style>
          </span>
        ) : (
          message.content
        )}
      </div>

      {/* Tool calls display - [Task]: C3 */}
      {showToolCalls &&
        message.toolCalls &&
        message.toolCalls.length > 0 && (
          <div
            style={{
              maxWidth: '80%',
              marginTop: '8px',
            }}
          >
            {message.toolCalls.map((tool, index) => (
              <div
                key={index}
                style={{
                  marginBottom: '8px',
                  borderRadius: '8px',
                  border: '1px solid #e5e7eb',
                  overflow: 'hidden',
                  fontSize: '13px',
                }}
              >
                {/* Tool header */}
                <button
                  onClick={() => toggleTool(index)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    backgroundColor: '#f3f4f6',
                    border: 'none',
                    cursor: 'pointer',
                    textAlign: 'left',
                  }}
                >
                  <span
                    style={{
                      transform: expandedTools.has(index)
                        ? 'rotate(90deg)'
                        : 'rotate(0deg)',
                      transition: 'transform 0.2s',
                    }}
                  >
                    ▶
                  </span>
                  <span
                    style={{
                      fontFamily: 'monospace',
                      fontWeight: '600',
                      color: '#3b82f6',
                    }}
                  >
                    {tool.name}
                  </span>
                  {tool.result && (
                    <span
                      style={{
                        marginLeft: 'auto',
                        padding: '2px 8px',
                        borderRadius: '4px',
                        backgroundColor: tool.result.success
                          ? '#d1fae5'
                          : '#fee2e2',
                        color: tool.result.success ? '#10b981' : '#ef4444',
                        fontSize: '11px',
                        fontWeight: '600',
                      }}
                    >
                      {tool.result.success ? 'SUCCESS' : 'ERROR'}
                    </span>
                  )}
                </button>

                {/* Tool details (expanded) */}
                {expandedTools.has(index) && (
                  <div
                    style={{
                      padding: '12px',
                      borderTop: '1px solid #e5e7eb',
                      backgroundColor: '#ffffff',
                    }}
                  >
                    {/* Arguments */}
                    <div style={{ marginBottom: '12px' }}>
                      <div
                        style={{
                          fontSize: '11px',
                          fontWeight: '600',
                          color: '#6b7280',
                          marginBottom: '4px',
                          textTransform: 'uppercase',
                        }}
                      >
                        Arguments
                      </div>
                      <pre
                        style={{
                          margin: 0,
                          padding: '8px',
                          borderRadius: '4px',
                          backgroundColor: '#f3f4f6',
                          fontSize: '12px',
                          fontFamily: 'monospace',
                          overflow: 'auto',
                          maxHeight: '100px',
                        }}
                      >
                        {formatToolArgs(tool.args)}
                      </pre>
                    </div>

                    {/* Result */}
                    {tool.result && (
                      <div>
                        <div
                          style={{
                            fontSize: '11px',
                            fontWeight: '600',
                            color: '#6b7280',
                            marginBottom: '4px',
                            textTransform: 'uppercase',
                          }}
                        >
                          Result
                        </div>
                        <pre
                          style={{
                            margin: 0,
                            padding: '8px',
                            borderRadius: '4px',
                            backgroundColor: tool.result.success
                              ? '#d1fae5'
                              : '#fee2e2',
                            fontSize: '12px',
                            fontFamily: 'monospace',
                            overflow: 'auto',
                            maxHeight: '150px',
                          }}
                        >
                          {tool.result.error ||
                            formatToolArgs(tool.result.data)}
                        </pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

      {/* Timestamp */}
      <div
        style={{
          fontSize: '11px',
          color: '#9ca3af',
          marginTop: '4px',
          paddingLeft: isUser ? '0' : '8px',
          paddingRight: isUser ? '8px' : '0',
        }}
      >
        {message.timestamp.toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        })}
      </div>
    </div>
  );
}

/**
 * MessageList displays all chat messages with auto-scroll.
 */
export function MessageList({
  messages,
  showToolCalls = true,
}: MessageListProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div
      ref={containerRef}
      style={{
        flex: 1,
        overflowY: 'auto',
        padding: '16px',
        backgroundColor: '#ffffff',
      }}
    >
      {messages.length === 0 ? (
        <div
          style={{
            textAlign: 'center',
            padding: '48px 16px',
            color: '#6b7280',
          }}
        >
          <div
            style={{
              width: '64px',
              height: '64px',
              backgroundColor: '#ede9fe',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 16px',
              fontSize: '28px',
            }}
          >
            💬
          </div>
          <h3
            style={{
              fontSize: '18px',
              fontWeight: '600',
              color: '#1f2937',
              marginBottom: '8px',
            }}
          >
            Start a conversation
          </h3>
          <p style={{ fontSize: '14px', maxWidth: '300px', margin: '0 auto' }}>
            Ask me to create, list, update, or delete your todos. For example:
            &quot;Add a task to buy groceries&quot;
          </p>
        </div>
      ) : (
        messages.map((message) => (
          <Message
            key={message.id}
            message={message}
            showToolCalls={showToolCalls}
          />
        ))
      )}
    </div>
  );
}

export default MessageList;
