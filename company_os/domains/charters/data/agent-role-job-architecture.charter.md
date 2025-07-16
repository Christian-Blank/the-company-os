Self-Evolving OS: Agents, Roles, Jobs, Design Document

Vision

Create a self-evolving Operating System (OS) that harmoniously integrates human and AI agents through a structured framework, enabling continuous self-improvement, enhanced productivity, and alignment of tasks with personalized and optimized working styles.

⸻

Guiding Principles
	1.	Agent Agnosticism: Roles and tasks should be clearly defined independently from execution agents (human or AI).
	2.	Personalized Optimization: Individual execution profiles tailored to the cognitive styles and strengths of agents.
	3.	Continuous Evolution: The system dynamically learns, updates, and adapts based on real-world feedback and analytics.
	4.	Transparency & Control: Agents (especially humans) have full visibility and the ability to adjust their own profiles.
	5.	Ease of Interaction: Human agents engage naturally with the OS, with internal structuring abstracted away by agents.

⸻

Mental Models
	•	Decoupled Definition Framework:
	•	Role Definition (“What”): Stable, abstract descriptions of tasks.
	•	Execution Profile (“How”): Personalized methodologies and instructions.
	•	Living “Me Manual”:
	•	Continuously evolving user-centric manuals guiding self-awareness and productivity.
	•	Feedback Loop & Iteration:
	•	Structured mechanisms for integrating peer feedback, self-reflection, and analytical insights.

⸻

V0 Schema Structure (YAML / Markdown)

Role Definition Schema (YAML)

role_id: unique_role_identifier
name: Role Name
purpose: Concise mission statement
capabilities:
  - capability_1
  - capability_2
boundaries:
  - boundary_rule_1
  - boundary_rule_2
tools_apis:
  allowed:
    - tool_1
    - api_1
output_schema:
  format: JSON/YAML/Markdown
  example: |
    {
      "key": "value"
    }

Execution Profile Schema (YAML)

Human Example

agent_id: unique_agent_identifier
agent_type: human
name: Agent Name
cognitive_style: intuitive | observant | analytical
experience_level: junior | intermediate | senior
preferred_methods:
  initial_approach: graph_brain_dump | linear_top_down
  frameworks:
    - JTBD
    - Hexagonal Architecture
personalized_guidance:
  reminders:
    - initial_brain_dump: true
    - multi_pass_refinement: true
feedback_history:
  - feedback_entry_id
analytics_insights:
  - insight_entry_id

AI Example

agent_id: unique_agent_identifier
agent_type: ai
model: Gemini 2.5 Pro | Claude 3.5 Sonnet
system_prompt_strategy: explicit_role | direct_instructions
interaction_style: chain_of_thought | few_shot
format_preferences: XML | Markdown | JSON
invocation_parameters:
  temperature: 0.1
  top_p: 0.95
model_strengths:
  - logical_reasoning
  - deterministic_tasks
model_weaknesses:
  - creative_tasks


⸻

Profile Creation, Extension, and Revision Mechanisms

Creation
	•	Initial Human Input:
	•	Human agents draft their own “Me Manual” in Markdown; AI converts this into structured YAML.
	•	AI agents receive initial tuning profiles based on experimentation.

Extension & Refinement
	•	Peer Feedback:
	•	Structured surveys and peer review, analyzed for specific insights.
	•	Self Feedback:
	•	Regular self-reflection exercises documented and processed.
	•	Behavioral Analytics:
	•	Automated collection and analysis of task interactions, outputs, and outcomes.
	•	Work Analysis:
	•	Analysis of timelines, deliverables, and commit history to extract productivity signals.
	•	LLM & Human Comparative Analysis:
	•	Comparison between task outcomes and agent profiles to find best-performing practices.

Revision & Syncing
	•	Continuous automatic updating of YAML profiles based on signals.
	•	Regular syncing of structured YAML back to human-readable Markdown for ease of human review and editing.

⸻

Task Profiling and Job Description Crystallization
	•	Functional & Non-Functional Requirements:
	•	Explicit input from experienced humans when initially defining tasks.
	•	Historical Analysis:
	•	Extract common denominators and refine definitions based on previous task executions.
	•	Dynamic Job Descriptions:
	•	Roles and specializations (e.g., “AI Engineer”) dynamically emerge based on analytical justification from task complexity, technology involved, and anticipated project needs.

⸻

System Workflow Overview
	1.	Define and maintain abstract Role Definitions.
	2.	Assign Roles dynamically to either AI or human agents.
	3.	Agents execute tasks guided by their personalized Execution Profiles.
	4.	Collect performance and behavior data as signals.
	5.	Analyze and refine signals into insights to continuously update Execution Profiles.
	6.	Maintain human-readable “Me Manuals” and structured YAML schemas in sync for transparency and ease of use.
	7.	Continuously iterate and refine system based on real-world experimentation and user feedback.

System Prompt Design & Integration

Prompt Layers
	1.	Role Prompt (Job Description) – Communicates the “WHAT”. It is generated from the Role Definition YAML and remains stable across agents.
	2.	Agent System Prompt – Communicates the “HOW”. Pulled from the Execution Profile.
	•	AI Agents: system_prompt field with explicit instructions, formatting rules, temperature, etc.
	•	Human Agents: onboarding_prompt field written in natural language; can be delivered via docs, chat, or UI hints.
	3.	Task-Specific Prompt (Context Builder) – Injects real-time context (files, requirements, deadlines, acceptance criteria) at runtime.

Schema Additions

Role Definition

role_prompt_template: |
  You are the **{{role_name}}**.
  Mission: {{purpose}}
  Capabilities: {{capabilities | join(', ')}}
  Boundaries: {{boundaries | join('; ')}}
  Tools available: {{tools_apis.allowed | join(', ')}}
  Output format: {{output_schema.format}}

Execution Profile – AI

system_prompt: |
  {{role_prompt}}
  ---
  Follow the guidelines below to excel:
  - Interaction style: {{interaction_style}}
  - Format preference: {{format_preferences}}
  - Invocation parameters: T={{invocation_parameters.temperature}}, P={{invocation_parameters.top_p}}

Execution Profile – Human

onboarding_prompt: |
  Hey {{name}}! Based on your **{{cognitive_style}}** working style, start with {{personalized_guidance.reminders[0]}}.
  Remember to leverage {{preferred_methods.frameworks | join(', ')}}.
  Your immediate goal: deliver output matching {{role_prompt.output_schema.format}}.

Prompt Generation Workflow
	1.	Compile Role Prompt from Role YAML.
	2.	Merge with Agent-specific System/Onboarding Prompt.
	3.	Inject Task Context (files, requirements) via a Context Builder service.
	4.	Deliver to AI via API or to Human via UI/chat/document.

Revision & Versioning
	•	Prompts are version-controlled alongside YAML.
	•	Any schema change triggers regeneration of prompt templates.
	•	Feedback loops (peer/self/analytics) can suggest prompt tweaks, which are merged through Pull Requests.

Precedence Rules
	1.	Task-specific context overrides agent system prompt.
	2.	Agent system/onboarding prompt overrides role prompt for execution details.
	3.	Role prompt remains canonical for mission & boundaries.

⸻
