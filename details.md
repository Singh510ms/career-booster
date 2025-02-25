Below is a **Product Requirements Document (PRD)** for the **Multi-Agent “Career Booster”** project (Idea 1). It’s designed with a scope you can realistically tackle in a 6-hour hackathon, leveraging **Cerebras.ai** (for LLM inference) and **CrewAI** (for agent orchestration).

---

# 1. **Overview**

## 1.1 Project Name
**Career Booster** – A Multi-Agent System that helps job seekers create relevant portfolio projects tailored to specific job descriptions.

## 1.2 Purpose
Many applicants struggle to demonstrate the exact skills that job descriptions demand. By providing:
1. **Project Ideation** based on job requirements and the applicant’s skills.
2. **Actionable Roadmap** to build those projects.

This system aims to lower the barrier to creating real-world, tangible portfolio pieces that impress potential employers.

## 1.3 Goals & Key Outcomes
- **Goal A**: Make it easy for a job seeker to come up with projects aligned to a job description.  
- **Goal B**: Provide a step-by-step plan to build each project, ensuring the seeker can confidently start coding.  
- **Outcome**: A short, guided pipeline that proves a candidate’s skills to recruiters in a more concrete way than a CV alone.

---

# 2. **Target Users**

1. **Job Seekers**: 
   - Individuals applying for software / data / tech roles who want relevant project ideas to strengthen their portfolios.
   - Have at least some coding familiarity but need guidance and structure.  
2. **Career Changers / Students**: 
   - People transitioning into tech and not sure how to demonstrate new skills.  
3. **Hiring Managers** (indirect benefit): 
   - They receive higher-quality portfolios and targeted projects from candidates.

---

# 3. **Product Scope & Features**

We’ll focus on **two core agents** (due to the 6-hour time constraint), with optional extensions if time allows.

## 3.1 **Agent 1: Project Ideation Agent**
**Input**  
- Job Description (text)  
- Candidate’s Skills / Interests (text)  

**Output**  
- 2–3 short project ideas relevant to the given job description.  
- Each idea includes:
  1. **Project Overview** (a one-liner describing what it is)
  2. **Key Tech Tools / Skills** used
  3. **Unique Selling Point** (why it would stand out)

**LLM Prompt Strategy**  
- We’ll instruct Cerebras’s LLM to parse the job requirements & candidate’s skill set, then produce bullet-pointed project ideas.
- Example prompt snippet:
  ```
  "You are an expert career consultant. Given the job description [JD] and candidate's skills [SKILLS], 
   propose 2-3 project ideas that can be built in under 2 weeks. Each idea should describe what the project does, 
   which tools it showcases, and how it aligns with the JD requirements."
  ```

## 3.2 **Agent 2: Project Planner & Roadmap Agent**
**Input**  
- A chosen project idea (text from the output of Agent 1).  
- Desired timeframe (e.g., 1 or 2 weeks).  

**Output**  
- A day-by-day (or milestone-based) **roadmap** with tasks, approximate time needed, and recommended tools (if relevant).
- The user sees an **actionable checklist** they can follow to build the project.

**LLM Prompt Strategy**  
- The system instructions can be:
  ```
  "You are a Project Planner Agent. Given this project idea [PROJECT_IDEA], create a step-by-step plan. 
   Organize it by days or major milestones. For each step, include a short description, tools needed, and estimated time to complete."
  ```

## 3.3 **(Optional) Agent 3: Resource Finder Agent**
- If time allows, this agent would take each step from the roadmap and suggest relevant tutorials, documentation links, or reference code.  
- This might require a curated resource library or an open web search.  

## 3.4 **(Optional) Agent 4: Project Review & Polish Agent**
- Takes the user’s code snippet or README.
- Outputs a short critique, highlighting alignment with the job description and best-practice improvements.

---

# 4. **Technical Architecture**

## 4.1 High-Level Flow
1. **Frontend** (Cursor-based UI or a simple web page):
   - User inputs job description + skills → Press **Generate Ideas** → Receives project ideas.
   - User picks a project → Press **Plan Project** → Receives step-by-step roadmap.
2. **Backend / Agent Orchestration** (CrewAI):
   - CrewAI handles the logic of calling the Cerebras LLM with carefully crafted prompts.
   - Each “agent” is essentially a unique system prompt or persona, separated by route or function.  
3. **LLM Inference** (Cerebras.ai):
   - The calls to the model happen through Cerebras’s API or inference endpoint.
   - Return structured or semi-structured text (JSON or bullet points) back to the UI.

## 4.2 Data Flow Diagram (Simplified)

```
User Input (JD + Skills)  -->  Frontend (HTTP request)  -->  Agent 1 (CrewAI / Cerebras)
                  <-- Output (Project Ideas)  <--
                               |
                               v
            User selects a Project Idea --> Agent 2 (CrewAI / Cerebras)
                                 <-- Output (Roadmap / Steps) <--
```

---

# 5. **User Flows**

### 5.1 **User Flow 1: Generate Project Ideas**
1. **User visits the web page**  
   - Sees two text fields: “Job Description” & “Your Skills.”
2. **User types/pastes text**  
   - “Backend Developer, 2–3 years’ experience, must know Node.js, etc.” for JD  
   - “Knows JavaScript, Node.js, basic React” for Skills
3. **User clicks “Generate Ideas”**  
   - The frontend sends a request to the backend (CrewAI).
4. **CrewAI calls Cerebras.ai LLM** with the prompt.  
5. **System returns** a list of 2–3 project ideas:
   - Example: “1) Real-time Node.js Chat App ... 2) Node.js + React Dashboard ...”
6. **User sees** the ideas on screen.

### 5.2 **User Flow 2: Get a Roadmap**
1. **User clicks “Plan This Project”** next to one of the generated ideas.
2. **Frontend** sends the chosen project idea to Agent 2.
3. **Agent 2** calls the LLM with a “Project Planner” prompt.
4. **System returns** a multi-step (or day-by-day) plan.
   - Each step has a short explanation and recommended tools.
5. **User sees** a neat checklist or timeline.

### 5.3 **(Optional) User Flow 3: Resource Finder / Review**
- If you have time to implement additional features, the user can click “Find Resources” or “Review My Code,” passing relevant text to Agents 3 or 4.

---

# 6. **Functional Requirements**

1. **User Interface**  
   - Text input fields for job description & skills.  
   - Display area for project ideas.  
   - Display area for the project roadmap.  
   - Minimal but user-friendly design (can be a single-page app in Cursor).

2. **CrewAI Integration**  
   - Each agent is a separate route or function with a distinct system prompt.  
   - Must store or pass user input between Agent 1 → Agent 2.

3. **Cerebras.ai LLM Calls**  
   - Must integrate with the model’s API endpoint.  
   - Ensure prompt clarity and error handling (e.g., if the model times out or returns partial output).

4. **Basic Error Handling**  
   - If the LLM fails, show a simple fallback message.  
   - Make sure the user can re-try generating ideas or roadmaps.

5. **Security**  
   - Basic protection so we don’t expose any sensitive keys.  
   - Possibly .env or environment variable for storing the Cerebras API key.

6. **Performance**  
   - The system should respond within a few seconds for each agent call.  
   - The data volumes are small (mostly text), so major performance concerns are minimal.

---

# 7. **Non-Functional Requirements**

1. **Reliability**  
   - We want stable performance, but a quick hackathon project can rely on cloud or local dev environment.
2. **Scalability**  
   - Not a huge concern for a hackathon MVP, but we can mention it if this concept is extended to handle large user traffic.
3. **Maintainability**  
   - Keep each agent’s prompt logic clean and separated.  
   - Document instructions or environment setup in a simple README.

---

# 8. **MVP Plan & Timeline (6-Hour Hackathon)**

1. **Hour 1**: 
   - Set up the basic UI skeleton in Cursor.  
   - Prepare environment variables / integration with Cerebras.ai.
2. **Hours 2–3**: 
   - Implement **Agent 1** (Project Ideation) route in CrewAI.  
   - Hard-code or quickly build the prompt with placeholders for JD + Skills.
   - Test end-to-end: user input → LLM call → response displayed.
3. **Hours 4–5**: 
   - Implement **Agent 2** (Project Planner).  
   - Pass the user’s chosen project idea as input.  
   - Return a structured roadmap output.  
   - Test / refine prompts for clarity.
4. **Hour 6**: 
   - Polish UI, handle any edge cases or errors.  
   - Add minimal styling for a more polished demo.  
   - If time remains, do a quick stab at either Resource Finder or a code review prompt.

---

# 9. **Success Metrics**

- **Functional Demo**  
  - User can input job description & skills → See 2–3 project ideas.  
  - User can pick an idea → Get a day-by-day plan.  
- **Clarity of Output**  
  - Are the project ideas relevant to the job description?  
  - Is the roadmap structured, with tasks and recommended tools?  
- **Presentation Readiness**  
  - Quick load times.  
  - Minimal or no crashes.  
  - Clear user flow for hackathon judges.

---

# 10. **Risks & Mitigations**

1. **Time Constraint (6 Hours)**  
   - **Mitigation**: Focus on Agents 1 and 2 only. Keep UI minimal.
2. **LLM Prompt Issues**  
   - **Mitigation**: Test prompts early; be specific about output format.
3. **Integration Complexity**  
   - **Mitigation**: If the Cerebras.ai or CrewAI integration is too complex, mock the calls or store example responses. Judges understand time constraints.
4. **Unclear / Rambling Outputs**  
   - **Mitigation**: Provide exemplars or a “role instruction” to the LLM to keep results concise.

---

## Final Remarks
This PRD outlines a **concise, two-agent MVP** that’s realistic for a short hackathon. By focusing on:
1. **Agent 1** → Project Ideation
2. **Agent 2** → Roadmap Planning

…you’ll produce a neat, end-to-end flow that can impress judges. If you manage time well, adding a **Resource Finder** or **Review Agent** can boost the “wow factor.” 