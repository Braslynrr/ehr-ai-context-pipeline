document.getElementById("sendBtn").addEventListener("click", async () => {
    const question = document.getElementById("questionInput").value;
    const patient = document.getElementById("patientSelect").value;
    const responseBox = document.getElementById("responseBox");

    if (!question || !patient) {
        alert("Please select a patient and write a question.");
        return;
    }

    let asnwer = await askQuestion(patient,question)

    // Placeholder para tu API Flask
    setTimeout(() => {
        responseBox.innerHTML += `
            <p><strong>Question:</strong> ${question}</p>
            <hr />
            <p><strong>Answer:</strong> ${asnwer}.</p>
        `;
    }, 200);
});


async function askQuestion(patientId, question) {
  try {
    const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        patient: patientId,
        question: question
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error("Error asking question:", error);
    return { error: "Failed to get response" };
  }
}