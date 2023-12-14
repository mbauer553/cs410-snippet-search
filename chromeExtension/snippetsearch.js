/*****************************************************/
/*      Handle Tab Change Logic of Extension         */
const searchTab = document.getElementById("searchTab");
const saveTab = document.getElementById("saveTab");
const searchTabContent = document.getElementById("search-container");
const saveTabContent = document.getElementById("save-container");

saveTabContent.style.display = "none";

searchTab.addEventListener("click", function () {
  // Show the "Search" tab content
  searchTabContent.style.display = "block";
  // Hide the "Save Snippet" tab content
  saveTabContent.style.display = "none";
});

saveTab.addEventListener("click", function () {
  // Show the "Save Snippet" tab content
  saveTabContent.style.display = "block";
  // Hide the "Search" tab content
  searchTabContent.style.display = "none";
});

const baseURL = 'http://<HOSTNAME>:<PORT>/'

/*****************************************************/
/*         Handle Search Logic                       */
let searchButton = document.getElementById('searchbutton');
let searchInput =  document.getElementById('searchtext');
const findURL = baseURL + 'findsnippet?lang=javascript&snippet='
searchButton.addEventListener(
    "click",
    function() {
        fetch(findURL+searchInput.value)
        .then(response => response.json())
        .then(
            function(data){
                // Clear old items from list
                const stringList = document.getElementById("stringList");
                while (stringList.firstChild) {
                  stringList.removeChild(stringList.firstChild);
                }

                // Write search results to list w/ clipboard copying shortcuts
                if (data.statusCode == 200 && data.body) {
                  items = data.body
                  console.log(items);
  
                  items.forEach((string) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = string;
                
                    const copyButton = document.createElement("button");
                    copyButton.textContent = "Copy";
                    copyButton.addEventListener("click", () => {
                      copyToClipboard(string);
                    });
                
                    listItem.appendChild(copyButton);                
                    stringList.appendChild(listItem);
                  });
                }
            }
        );
    },
    false
);

/*****************************************************/
/*         Handle Save Snippet Logic                 */

let saveButton = document.getElementById('savebutton');
let saveInput =  document.getElementById('savetext');
const saveURL = baseURL + 'addsnippet'
saveButton.addEventListener(
    "click",
    function() {
        fetch(saveURL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({"snippet": saveInput.value})
        })
        .then(response => response.json())
        .then(
            function(data){
              console.log(data);
            }
        );
    },
    false
);

/*****************************************************/

function copyToClipboard(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
}