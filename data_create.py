import json
import random
import os

def generate_tc_dataset(output_file="tnc_finetune_data.json", num_samples=100):
    # 1. Define Clause Modules: {Category: [ (Full Text, Summary Point, Risk Level) ]}
    # Risk Levels: 0 (Safe), 1 (Caution), 2 (Danger)
    clause_bank = {
        "Privacy": [
            ("We collect and store your precise GPS location data even when the application is not actively in use to improve local services.", "Continuous background location tracking.", 2),
            ("Your personal data, including browsing history, may be sold to third-party data brokers for advertising purposes.", "Data is sold to third-party brokers.", 2),
            ("We use industry-standard encryption to protect your data and do not share PII with external partners.", "Strong data encryption and no PII sharing.", 0),
            ("Automated systems analyze your private communications to detect prohibited content and serve relevant ads.", "Private messages are scanned for advertising.", 1)
        ],
        "Payments": [
            ("Subscriptions automatically renew at the end of each term unless cancelled via a written notarized letter.", "Auto-renewal with a difficult cancellation process.", 2),
            ("All sales are final. No refunds or credits will be issued for partially used subscription periods.", "Strict no-refund policy.", 1),
            ("Users are entitled to a full refund within 30 days if they are unsatisfied with the service quality.", "30-day money-back guarantee.", 0),
            ("We reserve the right to increase subscription fees at any time with 7 days' notice via the app dashboard.", "Short notice period for price hikes.", 1)
        ],
        "Liability": [
            ("You agree to waive your right to participate in a class-action lawsuit or a jury trial for any dispute.", "Mandatory individual arbitration; no class actions.", 2),
            ("Our total liability for any claim arising from the service is limited to $10.00 USD.", "Extremely low liability cap ($10).", 2),
            ("We are not responsible for any data loss resulting from server failures, hacking, or maintenance.", "No liability for data loss or security breaches.", 1),
            ("The company is liable for direct damages caused by gross negligence up to the amount paid in the last 12 months.", "Standard liability coverage for negligence.", 0)
        ],
        "Termination": [
            ("We may terminate your account at any time, for any reason, without prior notice or explanation.", "Immediate account termination without notice.", 2),
            ("If your account is terminated, all user-generated content will be permanently deleted and cannot be recovered.", "Irreversible loss of data upon termination.", 1),
            ("Users can export their data in a machine-readable format at any time before closing their account.", "Easy data portability and export options.", 0),
            ("Inactivity for more than 90 days results in the automatic deletion of all stored files.", "Short inactivity window before data deletion.", 1)
        ],
        "Rights": [
            ("You grant us a perpetual, irrevocable, worldwide license to modify and sell any content you upload.", "Company owns and can sell your uploaded content.", 2),
            ("You retain all ownership rights to your content but grant us a license to host it for service delivery.", "You retain ownership; platform gets hosting rights.", 0),
            ("We may use your username and likeness in promotional materials without additional compensation.", "Use of your identity for marketing without pay.", 1)
        ]
    }

    industries = ["Fintech", "Social Media", "SaaS", "E-commerce", "Gaming", "Health-Tech"]
    dataset = []

    for _ in range(num_samples):
        industry = random.choice(industries)
        
        # Pick 5 random categories to ensure we get exactly 5 points
        selected_categories = random.sample(list(clause_bank.keys()), 5)
        
        input_clauses = []
        summary_points = []
        keep_in_mind = []
        total_risk_score = 0
        
        for cat in selected_categories:
            clause_text, summary, risk = random.choice(clause_bank[cat])
            input_clauses.append(clause_text)
            summary_points.append(summary)
            total_risk_score += risk
            
            # If risk is high, add to "Keep in Mind"
            if risk >= 1:
                keep_in_mind.append(f"Carefully review the {cat.lower()} policy regarding {summary.lower().replace('.', '')}.")

        # Determine Recommendation based on risk score
        if total_risk_score >= 7:
            decision = "DECLINE"
            reasoning = "The terms contain multiple high-risk clauses regarding privacy and liability that heavily favor the provider."
        elif total_risk_score >= 3:
            decision = "PROCEED WITH CAUTION"
            reasoning = "While functional, there are notable concerns regarding data usage or termination rights."
        else:
            decision = "ACCEPT"
            reasoning = "These terms are standard for the industry and offer reasonable protections for the user."

        # Format the Input and Output strings
        full_input = f"[{industry} Terms of Service] " + " ".join(input_clauses)
        
        formatted_output = "### Key Agreements\n"
        for pt in summary_points:
            formatted_output += f"* {pt}\n"
            
        formatted_output += "\n### Things to Keep in Mind\n"
        if not keep_in_mind:
            formatted_output += "* No major red flags identified.\n"
        for kim in keep_in_mind[:2]: # Limit to 2 critical points
            formatted_output += f"* {kim}\n"
            
        formatted_output += f"\n### Recommendation\n* **Decision:** {decision}\n* **Reasoning:** {reasoning}"

        dataset.append({
            "instruction": "Summarize the following Terms and Conditions into 5 key points, highlight what to keep in mind, and provide a final recommendation.",
            "input": full_input,
            "output": formatted_output
        })

    # Save as JSON
    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Success! Generated {num_samples} samples in {output_file}")

# Generate 500 samples for a solid fine-tune
generate_tc_dataset(num_samples=50)