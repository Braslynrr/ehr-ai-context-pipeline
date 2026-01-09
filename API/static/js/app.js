document.getElementById("sendBtn").addEventListener("click", async () => {
    const questionInput = document.getElementById("questionInput");
    const question = questionInput.value;
    const patient = document.getElementById("patientSelect").value;
    const responseBox = document.getElementById("responseBox");
    const information = document.getElementById("notifyparagraph"); 
    const button = document.getElementById("sendBtn");

    if (!question || !patient) {
        alert("Please select a patient and write a question.");
        return;
    }

    responseBox.innerHTML += `
            <p><strong>Question:</strong> ${question}</p>
            <hr />`
             
    button.disabled = true;
    questionInput.value = ""
    information.innerText = "Loading your answer..."
    let asnwer = await askQuestion(patient,question)

    information.innerText = ""
    responseBox.innerHTML += `
            <p><strong>Answer:</strong> ${asnwer}.</p>
            <br>`;

    button.disabled = false;
    
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