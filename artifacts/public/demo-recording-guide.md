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

#### Scene 2: Initial Greeting (30 sec)

**Request:** "Hello"

Show:
- Tool call: `get_instruction()` → returns `init` state
- Response with menu: Review week, Plan learning, Assess stage, Debug blocker
- Explain: "The assistant calls the MCP server and receives instructions for the current state"

#### Scene 3: Stage Assessment Flow (1–1.5 min)

**Request:** "Assess my learning stage"

Show:
- Tool call: `get_instruction(state: "test_start")`
- Assistant asks diagnostic questions

**User response:** "I try to study every day but often lose the rhythm"

Show:
- Tool call: `get_instruction(state: "assess_stage")`
- Result: "Your stage: Practicing" with recommendations

#### Scene 4: Navigation & Architecture (30 sec)

**Request:** "Go back to start"

Show:
- Transition back to `init` state

Explain:
- "State transitions happen through explicit user actions"
- "FSM architecture: state → instruction → response → next state"

### 3. Conclusion

- Show that the session ends correctly
- Optionally show Developer console with tool calls

---

## Where to Host the Video

| Platform | How to Do It |
|----------|--------------|
| **Loom** | Free, fast, public link |
| **YouTube (unlisted)** | "Unlisted" — access by link |
| **Google Drive** | Access "Anyone with the link" |

---

## Checklist Before Submitting

- [ ] Video shows Developer Mode
- [ ] Tool calls to MCP server are visible
- [ ] At least 2–3 different states are shown
- [ ] State transition logic is explained
- [ ] Video is accessible via public link
- [ ] Duration is 2–4 minutes

---

## Example Tool Call

```json
{
  "name": "get_instruction",
  "arguments": {
    "state": "test_start"
  }
}
```

Response:
```json
{
  "state": "test_start",
  "instructions": "Ask diagnostic questions about learning habits...",
  "transitions": ["assess_stage", "init"]
}
```

---

## After Recording

1. Upload the video to your chosen platform
2. Copy the public link
3. Add the link to the OpenAI Apps form: **Demo Recording URL**

---

## Demo Video Link

**URL:** `[Add after recording]`

---

**Last Updated:** January 2, 2025
