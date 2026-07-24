# 🛡️ SlitherViz: Automated Smart Contract Audit System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![Next.js](https://img.shields.io/badge/Next.js-13%2B-black)
![Slither](https://img.shields.io/badge/Slither-Static_Analysis-red)

**SlitherViz** is a web-based, automated batch-processing framework designed to conduct static analysis on open Ethereum smart contracts. By integrating the **Slither Static Analyzer** and **Etherscan API**, this system allows researchers and developers to detect critical vulnerabilities (such as Reentrancy, arithmetic flaws, and access control issues) across multiple contracts concurrently, generating structured vulnerability mapping and an objective quantitative **Risk Score**.

This project was developed as a part of a research study on Ethereum Smart Contract Security and Reentrancy Vulnerabilities.

---

## 📸 Screenshots

*(Replace the image paths below with your actual screenshot files in your repository)*

### Dashboard Overview
![Dashboard Overview]<img width="1067" height="616" alt="Cuplikan layar 2026-07-22 231546" src="https://github.com/user-attachments/assets/f4aa07a8-53ad-44c8-aca7-1a2bbf4dd224" />
*Quantitative metrics, severity distribution (Donut Chart), and the top 5 most common vulnerabilities.*
<img width="753" height="678" alt="Cuplikan layar 2026-07-22 232526" src="https://github.com/user-attachments/assets/db7fee2e-c0f0-4beb-95ef-8fca35751d5a" />

### Audit Details & Vulnerability Mapping
![Audit Results]<img width="525" height="787" alt="Cuplikan layar 2026-07-22 232608" src="https://github.com/user-attachments/assets/5af33941-bf65-43a2-a7b4-63a7ce53aea2" />
*Deep dive into specific contract vulnerabilities, showing lines of code, severity levels, and specific attack vectors like `reentrancy-balance`.*

---

## ✨ Key Features

*   **Batch Processing Integration:** Audit multiple smart contract addresses (`0x...`) simultaneously without manual intervention.
*   **Asynchronous Pipeline & Rate Limiting:** Implements Token Bucket algorithms to bypass Etherscan Free Tier API limitations safely.
*   **Quantitative Risk Scoring:** Calculates an objective security score (0-100) based on weighted penalties for High, Medium, Low, and Informational findings.
*   **Interactive Analytics Dashboard:** Visualizes severity breakdowns and top vulnerabilities using modern, responsive charts.
*   **SWC Registry Mapping:** Maps Slither findings to standard security taxonomy for academic and professional reference.

---

## 🛠️ Tech Stack

**Backend:**
*   **Python 3**
*   **FastAPI** (High-performance asynchronous API framework)
*   **Slither** & **crytic-compile** (Core static analysis engine)

**Frontend:**
*   **Next.js / React** (User interface and client-side routing)
*   **Tailwind CSS** (Styling and layout)
*   **Recharts / Chart.js** (Data visualization)

---

## 🚀 Installation & Setup

### Prerequisites
*   Node.js (v16 or higher)
*   Python (3.8 or higher)
*   [Slither Analyzer](https://github.com/crytic/slither) installed globally or in your environment.
*   Etherscan API Key (Free tier is sufficient).

### 1. Clone the Repository
```bash
git clone [https://github.com/svjat4/SlitherViz-Smart-Contract-Audit-System.git](https://github.com/svjat4/SlitherViz-Smart-Contract-Audit-System.git)
cd SlitherViz-Smart-Contract-Audit-System
