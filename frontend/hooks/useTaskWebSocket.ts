/**
 * [Task]: T053
 * useTaskWebSocket - React hook for real-time task updates via WebSocket
 *
 * Phase V: Event-Driven Architecture
 * Provides real-time synchronization of task changes across browser tabs.
 */

import { useEffect, useRef, useCallback, useState } from 'react';

// WebSocket event types from backend
export type TaskEventType =
  | 'connection.established'
  | 'task.created'
  | 'task.updated'
  | 'task.completed'
  | 'task.deleted'
  | 'reminder.triggered'
  | 'pong';

export interface TaskEvent {
  type: TaskEventType;
  data: {
    taskId?: number;
    userId?: string;
    title?: string;
    changes?: Record<string, { old: any; new: any }>;
    [key: string]: any;
  };
}

export interface UseTaskWebSocketOptions {
  /** Callback when a task is created */
  onTaskCreated?: (data: TaskEvent['data']) => void;
  /** Callback when a task is updated */
  onTaskUpdated?: (data: TaskEvent['data']) => void;
  /** Callback when a task is completed */
  onTaskCompleted?: (data: TaskEvent['data']) => void;
  /** Callback when a task is deleted */
  onTaskDeleted?: (data: TaskEvent['data']) => void;
  /** Callback when a reminder fires */
  onReminderTriggered?: (data: TaskEvent['data']) => void;
  /** Callback for connection state changes */
  onConnectionChange?: (connected: boolean) => void;
  /** Enable automatic reconnection (default: true) */
  autoReconnect?: boolean;
  /** Reconnection interval in ms (default: 3000) */
  reconnectInterval?: number;
}

export interface UseTaskWebSocketReturn {
  /** Whether WebSocket is currently connected */
  isConnected: boolean;
  /** Last error message if any */
  error: string | null;
  /** Manually disconnect WebSocket */
  disconnect: () => void;
  /** Manually reconnect WebSocket */
  reconnect: () => void;
}

/**
 * Hook for subscribing to real-time task events via WebSocket
 *
 * @param token - JWT authentication token
 * @param options - Event handlers and configuration
 * @returns Connection state and control functions
 *
 * @example
 * ```tsx
 * const { isConnected } = useTaskWebSocket(token, {
 *   onTaskCreated: (data) => {
 *     console.log('New task:', data.taskId);
 *     refreshTasks();
 *   },
 *   onTaskUpdated: (data) => {
 *     console.log('Task updated:', data.taskId);
 *     refreshTasks();
 *   }
 * });
 * ```
 */
export function useTaskWebSocket(
  token: string | null,
  options: UseTaskWebSocketOptions = {}
): UseTaskWebSocketReturn {
  const {
    onTaskCreated,
    onTaskUpdated,
    onTaskCompleted,
    onTaskDeleted,
    onReminderTriggered,
    onConnectionChange,
    autoReconnect = true,
    reconnectInterval = 3000,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const pingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const shouldReconnectRef = useRef(true);

  // Get WebSocket URL from environment or derive from window location
  const getWebSocketUrl = useCallback(() => {
    if (!token) return null;

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = process.env.NEXT_PUBLIC_API_URL
      ? new URL(process.env.NEXT_PUBLIC_API_URL).host
      : window.location.host;

    return `${wsProtocol}//${host}/ws/tasks?token=${token}`;
  }, [token]);

  // Handle incoming WebSocket messages
  const handleMessage = useCallback(
    (event: MessageEvent) => {
      try {
        const message: TaskEvent = JSON.parse(event.data);

        switch (message.type) {
          case 'connection.established':
            setIsConnected(true);
            setError(null);
            onConnectionChange?.(true);
            break;

          case 'task.created':
            onTaskCreated?.(message.data);
            break;

          case 'task.updated':
            onTaskUpdated?.(message.data);
            break;

          case 'task.completed':
            onTaskCompleted?.(message.data);
            break;

          case 'task.deleted':
            onTaskDeleted?.(message.data);
            break;

          case 'reminder.triggered':
            onReminderTriggered?.(message.data);
            break;

          case 'pong':
            // Heartbeat response received
            break;
        }
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    },
    [
      onTaskCreated,
      onTaskUpdated,
      onTaskCompleted,
      onTaskDeleted,
      onReminderTriggered,
      onConnectionChange,
    ]
  );

  // Connect to WebSocket
  const connect = useCallback(() => {
    const url = getWebSocketUrl();
    if (!url) return;

    // Clean up existing connection
    if (wsRef.current) {
      wsRef.current.close();
    }

    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('[WebSocket] Connected');
        setError(null);

        // Start ping interval to keep connection alive
        pingIntervalRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }));
          }
        }, 30000);
      };

      ws.onmessage = handleMessage;

      ws.onerror = (event) => {
        console.error('[WebSocket] Error:', event);
        setError('WebSocket connection error');
      };

      ws.onclose = (event) => {
        console.log('[WebSocket] Closed:', event.code, event.reason);
        setIsConnected(false);
        onConnectionChange?.(false);

        // Clear ping interval
        if (pingIntervalRef.current) {
          clearInterval(pingIntervalRef.current);
          pingIntervalRef.current = null;
        }

        // Handle abnormal closure with reconnection
        if (
          autoReconnect &&
          shouldReconnectRef.current &&
          event.code !== 4001 // Don't reconnect on auth failure
        ) {
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log('[WebSocket] Attempting reconnection...');
            connect();
          }, reconnectInterval);
        }
      };
    } catch (e) {
      console.error('[WebSocket] Connection failed:', e);
      setError('Failed to connect to WebSocket');
    }
  }, [
    getWebSocketUrl,
    handleMessage,
    autoReconnect,
    reconnectInterval,
    onConnectionChange,
  ]);

  // Disconnect from WebSocket
  const disconnect = useCallback(() => {
    shouldReconnectRef.current = false;

    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (pingIntervalRef.current) {
      clearInterval(pingIntervalRef.current);
      pingIntervalRef.current = null;
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setIsConnected(false);
  }, []);

  // Reconnect to WebSocket
  const reconnect = useCallback(() => {
    shouldReconnectRef.current = true;
    disconnect();
    connect();
  }, [disconnect, connect]);

  // Connect on mount, disconnect on unmount
  useEffect(() => {
    if (token) {
      shouldReconnectRef.current = true;
      connect();
    }

    return () => {
      shouldReconnectRef.current = false;
      disconnect();
    };
  }, [token, connect, disconnect]);

  return {
    isConnected,
    error,
    disconnect,
    reconnect,
  };
}

export default useTaskWebSocket;
