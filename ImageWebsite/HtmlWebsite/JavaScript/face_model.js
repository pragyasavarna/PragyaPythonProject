Dropzone.autoDiscover = false;
let players = [];
function person_names(){
    fetch('/AIModel/artifacts/class_dictionary.json')
      .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
      })
      .then(data => {
      players = Object.keys(data);
      console.log("Players loaded:", players);

      // You can now build your dynamic table here
      const tableBody = document.getElementById("scoreTableBody");
      // 🧹 Clear the table first to prevent duplicates
      tableBody.innerHTML = "";
      players.forEach(name => {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.textContent = name;

        const scoreCell = document.createElement("td");
        scoreCell.id = `score_${name}`;
        scoreCell.textContent = `score_${name}`;

        row.appendChild(nameCell);
        row.appendChild(scoreCell);

        tableBody.appendChild(row);
      });
      })
      .catch(error => {
      console.error("Failed to load player data:", error);
      });
}
function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });
    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "/classify_image";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            /* 
            Below is a sample response if you have two faces in an image lets say virat and roger together.
            Most of the time if there is one person in the image you will get only one element in below array
            data = [
                {
                    class: "viral_kohli",
                    class_probability: [1.05, 12.67, 22.00, 4.5, 91.56],
                    class_dictionary: {
                        lionel_messi: 0,
                        maria_sharapova: 1,
                        roger_federer: 2,
                        serena_williams: 3,
                        virat_kohli: 4
                    }
                },
                {
                    class: "roder_federer",
                    class_probability: [7.02, 23.7, 52.00, 6.1, 1.62],
                    class_dictionary: {
                        lionel_messi: 0,
                        maria_sharapova: 1,
                        roger_federer: 2,
                        serena_williams: 3,
                        virat_kohli: 4
                    }
                }
            ]
            */
            console.log("Ankit");
            console.log(data);
            /*let players = ["Dad", "Tushar", "Rambir", "Ajay", "Pankaj", "Nandini", "Harsh", "Anju", "Harshit", "Deepak", "Prashant", "Vijender"];
            const tableBody = document.getElementById("scoreTableBody");

            players.forEach(name => {
              const row = document.createElement("tr");

              const nameCell = document.createElement("td");
              nameCell.textContent = name;

              const scoreCell = document.createElement("td");
              scoreCell.id = `score_${name}`;

              row.appendChild(nameCell);
              row.appendChild(scoreCell);

              tableBody.appendChild(row);
            });*/
            

            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
                        
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-player="${match.class}"`).html());
                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            }
            dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();
    person_names();
    init();
});