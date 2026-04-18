from services.rag import generate_answer   # your existing import

# === REAL RESUME AS CHUNKS (you can use 1 big chunk or split later) ===

chunks = [
    "Education: Kamla Nehru Institute of Technology, B.Tech CSE, 8.2/10, 2023–2027",
    
    "Work Experience: OneVarsity, Full Stack Developer Intern, Nov 2025 – Feb 2026\n• Full-Stack Development: Transitioned from React frontend to architecting backend...\n• Scalable Backend: Optimized database schemas and RESTful APIs for 100,000+ users\n• Technical Adaptability: 3-month pivot from UI/UX to backend",
    
    "Prescripto: Mern Stack, Cloudinary, Razorpay\n• Built doctor-patient platform with React, Node.js, MongoDB\n• JWT auth + role-based + bcrypt\n• Razorpay payment + Cloudinary\n• Tailwind + Admin/Doctor Dashboard",
    
    "Real-Time Chat Application: Socket.io, MERN\n• Real-time messaging + Zustand\n• Media sharing + MongoDB schema optimization",
    
    "Skills: Languages → C++, HTML, CSS, JS, Python\nFrameworks → React, Node, Express, Tailwind, Socket.io\nDB → MySQL, MongoDB\nFundamentals → DSA, OOPS, DBMS, OS",
    
    "Awards: Codechef 1484 • LeetCode 1705"
] # ← for now we use 1 chunk (you can split later)

stress_test_queries = [
    "Do I have any professional work experience?",
    "How many months of internship do I have?",
    "What backend technologies have I used in my internship?",
    "Do I know AWS or any cloud platform?",
    "Have I worked with Docker or Kubernetes?",
    "Tell me about my payment integration experience",
    "Do I have any fintech or banking domain experience?",
    "What is my current CGPA and in which year am I?",
    "List all my projects with their tech stack",
    "Do I know Python? Show proof from resume",
    "How many years of experience do I have in Node.js?",
    "Generate 5 technical interview questions for a Full Stack role based on my resume",
    "Rate my resume for a Fresher Full-Stack Developer position out of 10 and explain why",
    "What should I add to my resume to target SDE-1 roles at product companies?",
    "Have I built anything with authentication and authorization?"
]

  # keep the same list

print("🚀 Round-2 Stress Test with FIXED Prompt + Smart Chunks")

for i, q in enumerate(stress_test_queries, 1):
    result = generate_answer(q, chunks)
    print(f"{i:02d}) {q}")
    print("Answer    :", result["answer"])
    print("Sources   :", result["sources"])
    print("Confidence:", result["confidence"], result["confidence_label"])
    print("="*90)