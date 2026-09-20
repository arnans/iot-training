# Worksheet field clarity — 20 September 2026

Reviewed all 124 distinct answer keys across preparation, Activities 1–8, and the record sheet.
The current numbering is respected: Activity 6 is History, 7 is Dashboard, 8 is Design.
Changed unclear prompts in the task summaries, detailed procedures and record sheet together.

| Area | Clarification applied |
|---|---|
| Identification | Full board name versus IP address; omit `http://` from IP boxes; WiFi suffix accepts red/green/blue; distinguish the two VM-address entries. |
| Sensor observations | Light values and thresholds carry lux; float fields explicitly request ON/OFF from the board web page; sensor-response delay is in seconds. |
| Light rules | Numeric threshold is identified as a setting, including 4.1; written-rule fields identify the comparison and resulting command; distinguish toggle counts from full test cycles. |
| Time exercises | Use 24-hour clock examples; identify the time recorded; distinguish predictions before adding the time trigger from observations after adding it; name the Traces evidence required and permit “ไม่พบรอบการทำงาน”. |
| Watering | 4.7 explicitly reviews the original room measurement rather than overwriting it with a threshold; start/stop thresholds retain separate keys; state the conditions of the Manual/Auto observation. |
| Failure lab | Define the pre-fix symptom, post-fix pass criterion, screen/physical observations and supporting evidence. “สำเร็จ” now clearly refers to reproducing the problem; “แก้ได้” refers to passing the rule test. |
| Maintenance | Plan for a real farm: role responsible, inspection frequency and what/how to inspect, rather than classroom team-member names. |
| History | Request the changed variable/state, graph time, likely experiment and farm response separately. Permit uncertainty about cause and identify the source graph. |
| Dashboard | Request names of information/states and user commands, rather than current readings. Identify intended users by role. |
| Farm design | Scenario letter, problem/impact, sensor type and measurement, actuator, communication method and site-specific reason, separate power sources, backup duration, and battery choice/reason. Distinguish test procedure from observable acceptance criteria. |

4.1's existing field stores the numeric light threshold, not a yes/no confirmation. It therefore
remains numeric, with an explicit label and unit. Existing categorical answers already use radio
buttons. Text fields with a constrained vocabulary now state that vocabulary in the visible prompt.

No answer keys, control types or radio values changed, so existing saved answers remain compatible.
No new participant questions were introduced. Wording and context were improved around existing
questions; Activity 4's detailed closing question was aligned with its summary and record sheet.

Validation: compare answer schema against HEAD and check identical keys use consistent controls;
regenerate all participant HTML; run field synchronization/persistence/record-sheet-transfer checks,
procedure numbering and anchor checks, and the existing progress tests. The numbering test's heading
pattern was extended to Activity 8, which was listed but previously checked zero procedures.
This work does not resolve the remaining progress-completion or hardware-readiness items.
