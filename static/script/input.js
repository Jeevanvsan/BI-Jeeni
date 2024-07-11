const transitionDuration = 50; 
const delayBetweenNumbers = 5; 

function samp()
    {
      var fileInput = document.getElementById('file');
      var txt = document.getElementById('dark');
      var selectedFile = fileInput.files;
      if (selectedFile) {
        txt.innerHTML = "files uploaded"
        console.log('Selected file: ' + fileInput.files);

        // for (var i = 0; i < selectedFile.length; i++) {
        //   console.log('Selected file: ' + selectedFile[i].name);
        // }
      } else {
        showFlashMessage("No file found!", "Error");
        console.log('No file selected');
      }
    }

function showFlashMessage(message, type) {
      const flashContainer = document.getElementById('flash-messages');
      const flashMessage = flashContainer.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert" >\
      <p id="alert"> ${message} </p><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
      flashContainer.appendChild(flashMessage);
      setTimeout(() => {
          flashContainer.removeChild(flashMessage);
      }, 5000);
  }

async function runfn(event){
    event.preventDefault();
    console.log(11111111111111111)
    samp()
    const file_list = ["xlr", "pbit"]
    var fileInput = document.getElementById('file');
    var flag = true
    if (fileInput.files.length > 0){
      var selectedFile = fileInput.files;
      for (var i = 0; i < selectedFile.length; i++) {
          console.log('Selected file: ' + selectedFile[i].name);
          if (file_list.includes(selectedFile[i].name.split(".")[1])){
            // updateRandomText();
            // document.getElementById("loader").style.display = "inline";
            // setInterval(updateRandomText, 5000);
            // setTimeout(function () {transitionNumbers(1, 12);}, transitionDuration);
            // await startUpload(selectedFile[i]);
          }
          else
          {
                flag = false
                showFlashMessage(`${selectedFile[i].name} : Unsupported file format !`, "Error");
          }
        }

        
    }
    else{
      console("file error");
    }

    if (flag){
      await startUpload(selectedFile);
    }
}

async function sendfiles(selectedFile){
  try{
    var data = new FormData()

    for (var i = 0; i < selectedFile.length; i++) {
      data.append("file", selectedFile[i])
    }

    const response1 = await fetch(`/filereceive`,{
      method: "POST",
      body: data
    });
  }
  catch (error) {
    console.error('Error:', error);
}

}

async function startUpload(selectedFile) {
  try {
    var data = new FormData()
    for (var i = 0; i < selectedFile.length; i++) {
      data.append("file", selectedFile[i])
    }    
    console.log("Uploading...");
    updateRandomText();
    document.getElementById("loader").style.display = "inline";
    setInterval(updateRandomText, 5000);
    // console.log(selectedFile.name.split(".")[1]);
    // if ("xlr" == selectedFile.name.split(".")[1]) {
    //   // const response1 = await fetch(`/upload1/${selectedFile.name}`);
    //   // const data = await response1.json();
    //   // console.log('Data from /get_data:', data);
    //   // setTimeout(function () {transitionNumbers(20, 50);}, transitionDuration);
    //   // await upload2(data);
    //   console.log('xlr');
    // }
    // else if ("pbit" == selectedFile.name.split(".")[1])
    // {
      setTimeout(function () {transitionNumbers(12, 20);}, transitionDuration);
      const response1 = await fetch(`/uploadpbit`,{
        method: "POST",
        body: data
      });
      // setTimeout(function () {transitionNumbers(20, 30);}, transitionDuration);
      const val = await response1.json();
      // setTimeout(function () {transitionNumbers(30, 40);}, transitionDuration);
      // console.log('Data from /get_data:', val);
      if ("done" == val.status){
        data = JSON.stringify(val.file);
        console.log(data);
        // setTimeout(function () {transitionNumbers(40, 45);}, transitionDuration);
         const res = await fetch(`/startrunning`,{
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
        },
          body: data
        });

        res.json().then(val1 => {
          // Use val1 here, it contains the parsed JSON data
          console.log(val1)
          if ("done" == val1.status)
          {
            submitForm();



            // fetch('/showfiles')
            // .then(response => {
            //     if (!response.ok) {
            //         throw new Error('Network response was not ok');
            //     }
            //     console.log(response)
            // })
            // .then(data => {

            //     console.log(data)
                
            // })
            // .catch(error => {
            //     console.error('Error fetching data:', error);
            //     // Handle errors here
            // });
          }
        });
        
      }
      //   setTimeout(function () {transitionNumbers(45, 48);}, transitionDuration);
      //   const val2 = await response2.json();
      //   setTimeout(function () {transitionNumbers(48, 51);}, transitionDuration);
      //   console.log('Data from /get_data:', val2);
      //   if ("done" == val2.status){
      //     setTimeout(function () {transitionNumbers(51, 55);}, transitionDuration);
      //     const response3 = await fetch(`/image_generate`,{
      //       method: "POST",
      //       body: data
      //     });
      //     setTimeout(function () {transitionNumbers(55, 60);}, transitionDuration);
      //     const val3 = await response3.json();
      //     setTimeout(function () {transitionNumbers(60, 65);}, transitionDuration);
      //     console.log('Data from /get_data:', val3);
      //     if ("done" == val3.status){
      //       setTimeout(function () {transitionNumbers(65, 70);}, transitionDuration);
      //       const response4 = await fetch(`/html_generate`,{
      //         method: "POST",
      //         body: data
      //       });
      //       setTimeout(function () {transitionNumbers(70, 75);}, transitionDuration);
      //       const val4 = await response4.json();
      //       setTimeout(function () {transitionNumbers(75, 80);}, transitionDuration);
      //       console.log('Data from /get_data:', val4);
      //       if ("done" == val4.status){
      //         setTimeout(function () {transitionNumbers(80, 85);}, transitionDuration);
      //         const response5 = await fetch(`/zip_generate`,{
      //           method: "POST",
      //           body: data
      //         });
      //         setTimeout(function () {transitionNumbers(85, 90);}, transitionDuration);
      //         const val5 = await response5.json();
      //         setTimeout(function () {transitionNumbers(90, 93);}, transitionDuration);
      //         console.log('Data from /get_data:', val5);
      //         if ("done" == val5.status){
      //           setTimeout(function () {transitionNumbers(93, 95);}, transitionDuration);
      //           const response6 = await fetch(`/graph_generate`,{
      //             method: "POST",
      //             body: data
      //           });
      //           setTimeout(function () {transitionNumbers(95, 96);}, transitionDuration);
      //           const val6 = await response6.json();
      //           setTimeout(function () {transitionNumbers(96, 98);}, transitionDuration);
      //           console.log('Data from /get_data:', val6);
      //           if ("done" == val5.status){
      //             setTimeout(function () {transitionNumbers(98, 100);}, transitionDuration);
      //             submitForm();
      //           }
      //         }
      //       }
      //     }
      //   }
      // }
      // else if ("fail" == val.status){
      //   document.getElementById("loader").style.display = "none";
      //   showFlashMessage("Unsupported file version ! (version supports upto 23.11)", "Error");
      // }
    // }
} catch (error) {
    console.error('Error:', error);
}
}

async function upload2(data1) 
{
  try{
    console.log(data1.file)
    const response2 =  await fetch(`/upload/${data1.file}`);
    const data =  await response2.text();
  setTimeout(function () {transitionNumbers(50, 70);}, transitionDuration);
    console.log('Data from /get_data:', data);
    if(data == "done"){
  setTimeout(function () {transitionNumbers(70, 100);}, transitionDuration);
      submitForm();
      console.log('done');
    }
  } catch (error) {
  console.error('Error:', error);
}
}

function submitForm() {
  const form = document.getElementById('sform');
  form.action = '/main_file';
  form.method = 'POST';
  form.submit();
}

function updateRandomText() {
  console.log('load screen')
  fetch('/get_random_row')
      .then(response => response.json())
      .then(data => {
          document.getElementById('tip_p').textContent = data["tip"];
      })
      .catch(error => console.error('Error fetching random row:', error));
}

  function updateNumber(currentNumber) {
    document.getElementById('prgs').innerText = currentNumber+" %";
    document.getElementById('progress_bar').style.width = currentNumber+"%";
  }

function transitionNumbers(start, end) {
    let currentNumber = start;
    function updateAndCheck() {
        updateNumber(currentNumber);
        if (currentNumber < end) {
            currentNumber++;
            setTimeout(updateAndCheck, delayBetweenNumbers);
        }
    }
    updateAndCheck();
}