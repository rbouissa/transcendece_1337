// import { fetching_data } from "./rendringData";
let data_user ;

export function getCookie(name) {
    // console.log("Trying to get cookie:", name);  // Log the cookie name you're looking for
    const value = `; ${document.cookie}`;
    // console.log("document.cookie:", document.cookie);  // Log the entire cookies string to check its contents
    const parts = value.split(`; ${name}=`);
    // console.log("split result:", parts);  // Log the result of splitting by the cookie name
    if (parts.length === 2) {
        const cookieValue = parts.pop().split(";").shift();
        // console.log("Found cookie:", cookieValue);  // Log the value of the cookie if found
        return cookieValue;
    }
    // console.log("Cookie not found");
    return null;
}
export async function get_data(){
    const access_token = getCookie('access_token');
    try{
        const response = await fetch('http://localhost:8000/api/user_data/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'Content-Type': 'application/json',
            },
        });
        if(response.ok){
            data_user = await response.json();
            console.log("hhhh-:>>",data_user);
            // render_profile(data);
            // return(data);
        }
        else{
            console.error('Failed to fetch data');
        }
    }
    catch(error){
        console.error('Error fetching data:', error);
    }
}

export function uploadAvatar()
{
    
    document.getElementById("avatarUpload").click();console.log("ghayhrblya3!!!");
}
document.getElementById('avatarUpload').addEventListener('change', function (event) {
    console.log("ghayhrblya!!!");
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('avatar').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// function render_data()
// {
//     if(data_user.image){
//     document.getElementById('avatar').src = data_user.image;
//     }
//     else{
//         document.getElementById('avatar').src = "images/avatar.png";
//     }
// }
// render_data();


window.uploadAvatar = uploadAvatar;

export async function send_editing_data()
{
    const access_token = getCookie('access_token');
    console.log("ghayhrblya2!!!");
    document.getElementById("profile-form").addEventListener('submit', async function (event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const fullname = document.getElementById('fullname').value;
        const avatar = document.getElementById('avatar').src;
        const password = document.getElementById('password').value;
        const data={};
        if(username){
            data.username = username;
        }
        if(email){
            data.email = email;
        }
        if(fullname){
            data.fullname = fullname;
        }
        if(avatar){
            data.avatar = avatar;
        }
        if(password){
            data.password = password
        }
        console.log(data);
        try{
            const response = await fetch('http://127.0.0.1:8000/api/',{
                method:'POST',
                headers:{
                    'Content-Type': 'application/json',
                    "Authorization": `Bearer ${accessToken}`
                },
                body: JSON.stringify(data),
            });
            if(response.ok){
                const responseData = await response.json();
                document.getElementById('update-resp').textContent ='Request send successfully to '+responseData.username;
            }
            else{
                const errorData = await response.json();
                document.getElementById('update-resp').textContent = errorData.error;
            }
        }
        catch(error){
            console.error('Error:', error);
            document.getElementById('update-resp').textContent = 'Network error. Please try again.';
        }
    });
}