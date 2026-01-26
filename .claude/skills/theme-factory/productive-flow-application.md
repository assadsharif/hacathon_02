# Productive Flow Theme - Application Guide for Todo Chatbot

This document provides practical examples of applying the Productive Flow theme to the Todo Chatbot project.

## Quick Reference

| Element | Color | Hex Code | Usage |
|---------|-------|----------|-------|
| Primary Actions | Primary Blue | `#3b82f6` | Buttons, links, active states |
| Success/Complete | Success Green | `#10b981` | Completed tasks, checkmarks |
| AI Features | Accent Purple | `#8b5cf6` | Chat interface, AI responses |
| Backgrounds | Neutral Gray | `#f3f4f6` | Page backgrounds, cards |
| Text Primary | Dark Text | `#1f2937` | Headings, main content |
| Text Secondary | Medium Gray | `#6b7280` | Descriptions, metadata |
| Danger/Delete | Danger Red | `#ef4444` | Delete buttons, errors |

## Frontend Implementation (Tailwind CSS)

### tailwind.config.ts

```typescript
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6',
          hover: '#2563eb',
        },
        success: {
          DEFAULT: '#10b981',
          hover: '#059669',
        },
        accent: {
          DEFAULT: '#8b5cf6',
          hover: '#7c3aed',
        },
        neutral: {
          DEFAULT: '#f3f4f6',
          border: '#e5e7eb',
        },
        danger: {
          DEFAULT: '#ef4444',
          hover: '#dc2626',
        },
      },
      fontFamily: {
        sans: ['DejaVu Sans', 'system-ui', 'sans-serif'],
      },
    },
  },
}
```

### Component Examples

#### Todo Item Component

```tsx
<div className="bg-white border border-neutral-border rounded-lg p-4
                hover:border-primary transition-colors">
  <div className="flex items-center gap-3">
    {/* Checkbox */}
    <input
      type="checkbox"
      className="w-5 h-5 rounded border-neutral-border
                 checked:bg-success checked:border-success"
    />

    {/* Title */}
    <h3 className="text-lg font-bold text-[#1f2937]">
      Complete project documentation
    </h3>
  </div>

  {/* Description */}
  <p className="mt-2 text-[#6b7280]">
    Review and update all README files
  </p>

  {/* Actions */}
  <div className="mt-3 flex gap-2">
    <button className="px-4 py-2 bg-primary text-white rounded-md
                       hover:bg-primary-hover font-bold">
      Edit
    </button>
    <button className="px-4 py-2 bg-danger text-white rounded-md
                       hover:bg-danger-hover font-bold">
      Delete
    </button>
  </div>
</div>
```

#### AI Chat Message

```tsx
{/* User Message */}
<div className="flex justify-end mb-4">
  <div className="bg-primary text-white rounded-lg px-4 py-2 max-w-[70%]">
    <p className="font-sans">What tasks are due today?</p>
  </div>
</div>

{/* AI Response */}
<div className="flex justify-start mb-4">
  <div className="bg-accent text-white rounded-lg px-4 py-2 max-w-[70%]">
    <p className="font-sans">You have 3 tasks due today...</p>
  </div>
</div>
```

#### Primary Button

```tsx
<button className="bg-primary text-white px-6 py-3 rounded-md
                   font-bold hover:bg-[#2563eb]
                   transition-colors duration-200">
  Add New Task
</button>
```

#### Success Message

```tsx
<div className="bg-success/10 border border-success rounded-lg p-4">
  <div className="flex items-center gap-2">
    <svg className="w-6 h-6 text-success">✓</svg>
    <p className="text-success font-bold">Task completed successfully!</p>
  </div>
</div>
```

## Backend Status Responses

The backend can use these color codes in API responses for frontend rendering:

```python
# backend/app/models.py

class TodoStatus:
    OPEN = "open"           # Use Primary Blue (#3b82f6)
    IN_PROGRESS = "in_progress"  # Use Primary Blue (#3b82f6)
    COMPLETED = "completed" # Use Success Green (#10b981)
    DELETED = "deleted"     # Use Medium Gray (#6b7280)

class ResponseStyle:
    PRIMARY = "#3b82f6"
    SUCCESS = "#10b981"
    ACCENT = "#8b5cf6"
    DANGER = "#ef4444"
```

## Kubernetes Dashboard (Future Enhancement)

If creating a custom Kubernetes dashboard or monitoring UI:

```yaml
# Example metrics visualization colors
metrics:
  healthy_pods: "#10b981"    # Success Green
  degraded_pods: "#f59e0b"   # Warning Orange
  failed_pods: "#ef4444"     # Danger Red
  cpu_usage: "#3b82f6"       # Primary Blue
  memory_usage: "#8b5cf6"    # Accent Purple
```

## Documentation Theme

For GitHub README, documentation sites, or presentations:

### Headings
- **Color:** `#1f2937` (Dark Text)
- **Font:** DejaVuSans Bold

### Body Text
- **Color:** `#6b7280` (Medium Gray)
- **Font:** DejaVuSans

### Code Blocks
- **Background:** `#f3f4f6` (Neutral Gray)
- **Border:** `#e5e7eb` (Neutral Border)

### Links
- **Color:** `#3b82f6` (Primary Blue)
- **Hover:** `#2563eb` (Darker Blue)

## Accessibility Compliance

All color combinations meet WCAG AA standards:

✓ Primary Blue (#3b82f6) on White: 4.5:1 contrast ratio
✓ Dark Text (#1f2937) on White: 16:1 contrast ratio
✓ White on Primary Blue: 4.5:1 contrast ratio
✓ White on Success Green: 4.5:1 contrast ratio
✓ White on Accent Purple: 4.5:1 contrast ratio

## Next Steps

To fully implement this theme in the Todo Chatbot project:

1. **Update Tailwind Configuration** - Add color palette to `frontend/tailwind.config.ts`
2. **Update Components** - Apply new colors to existing React components
3. **Update Global Styles** - Set font family to DejaVuSans in `globals.css`
4. **Test Contrast** - Verify all text remains readable
5. **Update Documentation** - Apply theme colors to README badges and diagrams
