/**
 * ChatWindow Component
 * [Task]: C1 - ChatKit UI component
 * [Task]: C2 - Connect to TodoAgent
 * [Task]: C3 - Display tool invocations
 * [Refs]: specs/phase-iii/plan.md#file-structure
 *
 * Main chat interface that combines MessageList and ChatInput,
 * handles message state, and connects to the TodoAgent.
 */

'use client';

import { useState, useCallback } from 'react';
import { ChatInput } from './ChatInput';
import { MessageList, ChatMessage, ToolCallDisplay } from './MessageList';
import {
  createTodoAgent,
  checkForRefusal,
  checkForClarification,
  TodoAgent,
} from '@/lib/agent';

interface ChatWindowProps {
  /** JWT token for authenticated API calls */
  token: string;
  /** Callback when chat updates todo list */
  onTodoChange?: () => void;
}

/**
 * Generate a unique message ID
 */
function generateMessageId(): string {
  return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * ChatWindow is the main chat interface component.
 * It manages conversation state and integrates with the TodoAgent.
 */
export function ChatWindow({ token, onTodoChange }: ChatWindowProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showToolCalls, setShowToolCalls] = useState(true);
  const [agent] = useState<TodoAgent>(() => createTodoAgent(token));

  /**
   * Process a user message through the TodoAgent.
   * [Task]: C2 - Agent integration
   */
  const processMessage = useCallback(
    async (userMessage: string) => {
      // Add user message to chat
      const userMsg: ChatMessage = {
        id: generateMessageId(),
        role: 'user',
        content: userMessage,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMsg]);

      // Add loading indicator
      const loadingId = generateMessageId();
      setMessages((prev) => [
        ...prev,
        {
          id: loadingId,
          role: 'assistant',
          content: '',
          timestamp: new Date(),
          isLoading: true,
        },
      ]);

      setIsProcessing(true);

      try {
        // Check for refusal patterns first
        // [Task]: B3 - Refusal logic integration
        const refusalResponse = checkForRefusal(userMessage);
        if (refusalResponse) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === loadingId
                ? {
                    ...m,
                    content: refusalResponse,
                    isLoading: false,
                  }
                : m
            )
          );
          return;
        }

        // Check for clarification patterns
        // [Task]: B3 - Clarification logic integration
        const clarificationResponse = checkForClarification(userMessage);
        if (clarificationResponse) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === loadingId
                ? {
                    ...m,
                    content: clarificationResponse,
                    isLoading: false,
                  }
                : m
            )
          );
          return;
        }

        // Process through intent detection and tool execution
        // [Task]: C2 - Connect to TodoAgent
        const { response, toolCalls } = await processUserIntent(
          userMessage,
          agent
        );

        // Update the loading message with the response
        setMessages((prev) =>
          prev.map((m) =>
            m.id === loadingId
              ? {
                  ...m,
                  content: response,
                  isLoading: false,
                  toolCalls: toolCalls,
                }
              : m
          )
        );

        // Notify parent if todos may have changed
        if (toolCalls && toolCalls.length > 0 && onTodoChange) {
          onTodoChange();
        }
      } catch (error) {
        // Handle errors
        const errorMessage =
          error instanceof Error
            ? error.message
            : 'Something went wrong. Please try again.';

        setMessages((prev) =>
          prev.map((m) =>
            m.id === loadingId
              ? {
                  ...m,
                  content: errorMessage,
                  isLoading: false,
                }
              : m
          )
        );
      } finally {
        setIsProcessing(false);
      }
    },
    [agent, onTodoChange]
  );

  /**
   * Clear conversation history
   */
  const clearChat = useCallback(() => {
    setMessages([]);
    agent.clearHistory();
  }, [agent]);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        backgroundColor: '#ffffff',
        borderRadius: '8px',
        boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
        overflow: 'hidden',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '16px',
          borderBottom: '1px solid #e4e6eb',
          backgroundColor: '#f7f8fa',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              backgroundColor: '#1877f2',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px',
            }}
          >
            🤖
          </div>
          <div>
            <h2
              style={{
                fontSize: '16px',
                fontWeight: '600',
                color: '#1c1e21',
                margin: 0,
              }}
            >
              Todo Assistant
            </h2>
            <p
              style={{
                fontSize: '13px',
                color: '#65676b',
                margin: 0,
              }}
            >
              {isProcessing ? 'Thinking...' : 'Online'}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Toggle tool calls - [Task]: C3 */}
          <button
            onClick={() => setShowToolCalls(!showToolCalls)}
            style={{
              padding: '8px 12px',
              borderRadius: '6px',
              border: '1px solid #e4e6eb',
              backgroundColor: showToolCalls ? '#e7f3ff' : 'transparent',
              color: showToolCalls ? '#1877f2' : '#65676b',
              fontSize: '13px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
            title={showToolCalls ? 'Hide tool calls' : 'Show tool calls'}
          >
            <span style={{ fontFamily: 'monospace' }}>&lt;/&gt;</span>
            Tools
          </button>

          {/* Clear chat */}
          <button
            onClick={clearChat}
            style={{
              padding: '8px 12px',
              borderRadius: '6px',
              border: '1px solid #e4e6eb',
              backgroundColor: 'transparent',
              color: '#65676b',
              fontSize: '13px',
              cursor: 'pointer',
            }}
            title="Clear conversation"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Messages */}
      <MessageList messages={messages} showToolCalls={showToolCalls} />

      {/* Input */}
      <ChatInput
        onSend={processMessage}
        disabled={isProcessing}
        placeholder="Ask me to manage your todos..."
      />
    </div>
  );
}

/**
 * Process user intent and execute appropriate tool.
 * [Task]: C2 - Agent integration with tool execution
 *
 * This is a simplified intent detection that maps common patterns
 * to tool calls. In production, this would use the OpenAI API
 * for more sophisticated intent recognition.
 */
async function processUserIntent(
  message: string,
  agent: TodoAgent
): Promise<{ response: string; toolCalls?: ToolCallDisplay[] }> {
  const lowerMessage = message.toLowerCase().trim();
  const toolCalls: ToolCallDisplay[] = [];

  // Intent: List todos
  if (
    lowerMessage.includes('list') ||
    lowerMessage.includes('show') ||
    lowerMessage.includes('what') ||
    lowerMessage.includes('my task') ||
    lowerMessage.includes('my todo') ||
    lowerMessage.match(/^(get|see|view)\s+(all\s+)?(my\s+)?(todo|task)/i)
  ) {
    // Check for status filter
    let statusFilter: 'active' | 'completed' | undefined;
    if (lowerMessage.includes('active') || lowerMessage.includes('pending')) {
      statusFilter = 'active';
    } else if (
      lowerMessage.includes('completed') ||
      lowerMessage.includes('done') ||
      lowerMessage.includes('finished')
    ) {
      statusFilter = 'completed';
    }

    const args = statusFilter ? { status: statusFilter } : {};
    const result = await agent.executeTool({
      id: 'call-1',
      type: 'function',
      function: {
        name: 'list_todos',
        arguments: JSON.stringify(args),
      },
    });

    toolCalls.push({
      name: 'list_todos',
      args,
      result,
    });

    return {
      response: agent.formatToolResult('list_todos', result),
      toolCalls,
    };
  }

  // Intent: Create todo
  if (
    lowerMessage.includes('add') ||
    lowerMessage.includes('create') ||
    lowerMessage.includes('new task') ||
    lowerMessage.includes('new todo')
  ) {
    // Extract title from message
    let title = message;

    // Remove common prefixes
    const prefixes = [
      /^(please\s+)?add\s+(a\s+)?(task|todo)\s+(to\s+)?/i,
      /^(please\s+)?create\s+(a\s+)?(new\s+)?(task|todo)\s+(to\s+)?/i,
      /^(please\s+)?make\s+(a\s+)?(new\s+)?(task|todo)\s+(to\s+)?/i,
      /^new\s+(task|todo)\s*:?\s*/i,
    ];

    for (const prefix of prefixes) {
      title = title.replace(prefix, '');
    }

    title = title.trim();

    if (!title) {
      return {
        response: 'Please provide a title for the task.',
        toolCalls: [],
      };
    }

    const args = { title };
    const result = await agent.executeTool({
      id: 'call-1',
      type: 'function',
      function: {
        name: 'create_todo',
        arguments: JSON.stringify(args),
      },
    });

    toolCalls.push({
      name: 'create_todo',
      args,
      result,
    });

    return {
      response: agent.formatToolResult('create_todo', result),
      toolCalls,
    };
  }

  // Intent: Mark as completed
  if (
    lowerMessage.includes('complete') ||
    lowerMessage.includes('done') ||
    lowerMessage.includes('finish') ||
    lowerMessage.includes('mark')
  ) {
    // Try to extract ID
    const idMatch = message.match(/(\d+)/);
    if (!idMatch) {
      return {
        response:
          'Which task would you like to mark as completed? Please specify the task ID.',
        toolCalls: [],
      };
    }

    const id = parseInt(idMatch[1], 10);
    const args = { id, status: 'completed' as const };

    const result = await agent.executeTool({
      id: 'call-1',
      type: 'function',
      function: {
        name: 'update_todo',
        arguments: JSON.stringify(args),
      },
    });

    toolCalls.push({
      name: 'update_todo',
      args,
      result,
    });

    return {
      response: agent.formatToolResult('update_todo', result),
      toolCalls,
    };
  }

  // Intent: Delete todo
  if (
    lowerMessage.includes('delete') ||
    lowerMessage.includes('remove') ||
    lowerMessage.includes('trash')
  ) {
    // Try to extract ID
    const idMatch = message.match(/(\d+)/);
    if (!idMatch) {
      return {
        response:
          'Which task would you like to delete? Please specify the task ID.',
        toolCalls: [],
      };
    }

    const id = parseInt(idMatch[1], 10);
    const args = { id };

    const result = await agent.executeTool({
      id: 'call-1',
      type: 'function',
      function: {
        name: 'delete_todo',
        arguments: JSON.stringify(args),
      },
    });

    toolCalls.push({
      name: 'delete_todo',
      args,
      result,
    });

    return {
      response: agent.formatToolResult('delete_todo', result),
      toolCalls,
    };
  }

  // Intent: Get specific todo
  if (
    lowerMessage.includes('get task') ||
    lowerMessage.includes('show task') ||
    lowerMessage.includes('details')
  ) {
    const idMatch = message.match(/(\d+)/);
    if (!idMatch) {
      return {
        response:
          'Which task would you like to see? Please specify the task ID.',
        toolCalls: [],
      };
    }

    const id = parseInt(idMatch[1], 10);
    const args = { id };

    const result = await agent.executeTool({
      id: 'call-1',
      type: 'function',
      function: {
        name: 'get_todo',
        arguments: JSON.stringify(args),
      },
    });

    toolCalls.push({
      name: 'get_todo',
      args,
      result,
    });

    return {
      response: agent.formatToolResult('get_todo', result),
      toolCalls,
    };
  }

  // Default: unclear intent
  return {
    response:
      "I can help you create, list, update, or delete todos. Try saying something like:\n• \"Show my tasks\"\n• \"Add a task to buy groceries\"\n• \"Mark task 1 as done\"\n• \"Delete task 2\"",
    toolCalls: [],
  };
}

export default ChatWindow;
