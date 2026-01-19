/**
 * Chat Components Module
 * [Task]: C1 - ChatKit UI components
 * [Refs]: specs/phase-iii/plan.md#file-structure
 *
 * Exports all chat-related components for Phase III.
 */

export { ChatWindow, default as ChatWindowDefault } from './ChatWindow';
export { ChatInput, default as ChatInputDefault } from './ChatInput';
export {
  MessageList,
  default as MessageListDefault,
  type ChatMessage,
  type ToolCallDisplay,
} from './MessageList';
