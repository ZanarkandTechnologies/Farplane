# How to Plan Frontend Features

## Before You Start
1. Identify existing components to reuse (shadcn, AI Elements).
2. Check theming requirements (dark mode, brand colors).
3. Determine responsive breakpoints needed.

## Planning Order
1. **Data requirements**: What props/state does the UI need?
2. **Component structure**: Container vs presentational.
3. **Interactions**: Loading states, error states, success feedback.
4. **Accessibility**: ARIA labels, keyboard navigation.

## Key Questions
- Is this a form, list, detail view, or dashboard?
- Does it need optimistic updates?
- Are there animations or transitions?

## Common Patterns
- Forms: schema validation → controlled inputs → submit handler
- Lists: data fetching → loading skeleton → empty state → items
- Modals: trigger → overlay → content → close handling
