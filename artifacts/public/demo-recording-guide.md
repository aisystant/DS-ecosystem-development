# Demo Recording Guide — Learning Copilot

Instructions for recording a demo video for OpenAI App Review.

---

## OpenAI Requirements

- **Format:** Video (Loom / YouTube unlisted / Google Drive)
- **Duration:** 2–4 minutes is sufficient
- **Mode:** Developer Mode in ChatGPT

---

## Recording Scenario

### 1. Preparation (do not record)

- Open ChatGPT in developer mode
- Connect the Learning Copilot app
- Make sure the MCP server is responding

### 2. Start Recording

#### Scene 1: Connection (30 sec)

Show:
- ChatGPT interface with the connected app
- The name "Learning Copilot" in the tools/actions list

#### Scene 2: Main Scenario (1.5–2 min)

**Request 1:** "Let's summarize the week"
```
User: Let's summarize the week
```
Show:
- Tool call to the MCP server
- Response with widget and action buttons
- Explain: "The assistant calls the fsm-mcp server and receives instructions for the current state"

**Request 2:** Clicking the "Go to start" button
```
User: [clicks "Go to start" button / types "Go to start"]
```
Show:
- Transition to the initial state
- New widget with greeting

**Request 3:** "Analyze a blocker"
```
User: Analyze a blocker
```
Show:
- The assistant offers to identify the blocker
- Dialog scenario

#### Scene 3: Help Scenario (30 sec)

**Request:** "How do I work with you?"
```
User: How do I work with you?
```
Show:
- Transition to help state
- Explanation of the assistant's capabilities

#### Scene 4: Architecture Explanation (30 sec)

Explain by voice or text:
- "State transitions only happen through ui.actions"
- "Markdown content does not contain transition commands — this is safe"
- "FSM architecture: state → instruction → response"

### 3. Conclusion

- Show that the session ends correctly
- You can show the Developer console with tool calls

---

## Where to Host the Video

| Platform | How to Do It |
|----------|--------------|
| **Loom** | Free, fast, public link |
| **YouTube (unlisted)** | "Unlisted" — access by link |
| **Google Drive** | Access "Anyone with the link" |
| **Cloudflare Stream** | If you have an account |

---

## Checklist Before Submitting

- [ ] Video shows Developer Mode
- [ ] Tool calls to MCP server are visible
- [ ] At least 2–3 different states are shown
- [ ] Transition logic through ui.actions is explained
- [ ] Video is accessible via public link
- [ ] Duration is 2–4 minutes

---

## Example Tool Call (for demonstration)

```json
{
  "name": "learning-copilot",
  "arguments": {
    "action": "get_instructions",
    "state": "weekly_review"
  }
}
```

Response:
```json
{
  "instructions": "...",
  "ui": {
    "actions": [
      {"label": "Go to start", "action": "go_home"},
      {"label": "Analyze blocker", "action": "analyze_block"}
    ]
  }
}
```

---

## After Recording

1. Upload the video to your chosen platform
2. Copy the public link
3. Add the link to the OpenAI Apps form: **Demo Recording URL**
4. Update this document with the final link

---

## Demo Video Link

**URL:** `[Add after recording]`

---

**Last Updated:** January 2, 2025
