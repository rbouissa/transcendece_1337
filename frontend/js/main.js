//all the routes are defined here
function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

const routes = [
    {link:'/',template:'landing.html'},
    {link:'/landing',template:'landing.html'},
    {link:'/login',template:'login.html'},
    {link:'/signup',template:'signup.html'},
    {link:'/dashboard',template:'dashboard.html'},
    {link:'/friends',template:'friends.html'},
    {link:'/leaderboard',template:'leaderboard.html'},
    {link:'/test' ,template:'test.html'},
];// Utility to get a cookie value
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
}

// Function to fetch user data
async function fetchUserData() {
    const accessToken = getCookie('access_token');

    if (!accessToken) {
        console.error("Access token not found");
        document.getElementById('userData').textContent = 'Access token not found';
        return;
    }

    try {
        console.log("Access token:", accessToken);

        const response = await fetch('http://localhost:8000/api/user_data/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const userData = await response.json();
            console.log('User data:', userData);
            document.getElementById('userData').textContent = JSON.stringify(userData, null, 2);
        } else if (response.status === 401) {
            
            console.warn('Access token expired. Attempting to refresh...');
            sleep(10000)
            const refreshToken = getCookie("refresh_token");

            if (refreshToken) {
                const refreshResponse = await fetch("http://localhost:8000/token_refresh/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ refresh: refreshToken }),
                });

                if (refreshResponse.ok) {
                    const data = await refreshResponse.json();
                    document.cookie = `access_token=${data.access}; SameSite=None; Secure; Path=/`;

                    console.log('Access token refreshed successfully');
                    // Retry the original request
                    return fetchUserData();
                } else {
                    console.error('Failed to refresh token');
                    document.getElementById('userData').textContent = 'Failed to refresh token';
                }
            } else {
                console.error('Refresh token not found. User needs to re-authenticate.');
                document.getElementById('userData').textContent = 'Please log in again.';
            }
        } else {
            console.error('Failed to fetch user data:', response.statusText);
            document.getElementById('userData').textContent = 'Failed to fetch user data';
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
        document.getElementById('userData').textContent = 'Error fetching user data';
    }
}

function handleFetchClick() {
    console.log('Fetching user data!!!!!!!!!');
    const accessToken = document.getElementById('accessToken').value;
    fetchUserData(accessToken);
}

window.handleFetchClick = handleFetchClick;






const content = document.getElementById('page-content');
const profile_content = document.getElementById('profiles-content');
let css_link = null;
const navbar = document.getElementById('landing-navbar');
const home_navbar = document.getElementById('home-navbar');
//function to handle navigation

export function handling_navigation(route,updateHistory = true){
    console.log("Route: ",route);
    const exact_route = routes.find(r => r.link === route);
    if(exact_route)
    {
        get_content(exact_route.template);
        if (updateHistory) {
            history.pushState({ route }, "", route);
        }
    }
    else{
        get_content('404.html');
        history.pushState({route},"",route);
    }
}

//function to get the content of the template

async function get_content(template){
    try{
        console.log("--->",template);
        const response = await fetch(`views/${template}`);
        if(response.ok){
            const data = await response.text();
            import(`./theme.js`).then(module => {
                module.toggleTheme();
            } ).catch(error => {
                console.error('Error in importing the module:', error);
            } );
            const css_file = template.split('.')[0];
            if(css_link){
               document.head.removeChild(css_link); 
            }
            css_link = document.createElement('link');
            css_link.rel = 'stylesheet';
            css_link.href = `css/${css_file}.css`;
            document.head.appendChild(css_link);
            // change_css(`css/${css_file}.css`);
            // console.log("CSS File: ",css_file);
            console.log("CSS Link: ",css_link);
            if(template==="login.html" || template==="signup.html")
            {
                navbar.style.display = "none";
                home_navbar.style.display = "none";
                if(template==="login.html"){
                import(`./authentication.js`).then(module => {
                    module.log42();
                    module.login();
                    module.handleCallbackResponse();
                }).catch(error => {
                    console.error('Error in importing the module:', error);
                } );
                }
                else if(template==="signup.html")
                {
                    import(`./authentication.js`).then(module => {
                        module.simplelog();
                    }).catch(error => {
                        console.error('Error in importing the module:', error);
                    } );
                    
                }
            }
            else if(template==="landing.html"){
                navbar.style.display = "block";
                home_navbar.style.display = "none";
            }
            else{
                navbar.style.display = "none";
                
                home_navbar.style.display = "block";
            }
            document.title = css_file;
            if(template==="landing.html" || template==="login.html" || template==="signup.html"){
                profile_content.style.display = "none";
                content.style.display = "block";
                content.innerHTML = data;
            }
            else{
                const navbar_css = document.createElement('link');
                navbar_css.rel = 'stylesheet';
                navbar_css.href = 'css/home.css';
                document.head.appendChild(navbar_css);
                content.style.display = "none";
                profile_content.style.display = "block";
                profile_content.innerHTML = data;
            }
        }
        else{
            throw new Error('Error in fetching the content');
        }
    }
    catch(error){
        content.innerHTML = `<h1>${error.message}</h1>`;
    }
}

//function to change the css file

function change_css(path) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = path;
    document.head.appendChild(link);
}


document.addEventListener("click", (event) => {
    let target = event.target;

    while (target && !target.hasAttribute("data-route"))
    {
        target = target.parentElement;
    }
    if (target && target.hasAttribute("data-route"))
    {
        event.preventDefault();
        const route = target.getAttribute("data-route");
        handling_navigation(route);
    }
});

window.addEventListener("popstate", (event) => {
    const route = event.state?.route || "/landing";
    console.log("Pop State: ",route);
    handling_navigation(route);
});

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM Content Loaded");
    const initialRoute = window.location.pathname || "/landing";
    handling_navigation(initialRoute, false);
});

// async function refreshAccessToken(refreshToken) {
//     try {
//         const response = await fetch('http://localhost:8000/api/token_refresh/', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ refresh: refreshToken }),
//         });

//         if (response.ok) {
//             const data = await response.json();
//             const newAccessToken = data.access;
//             console.log('New access token:', newAccessToken);
//             return newAccessToken;
//         } else {
//             console.error('Failed to refresh access token');
//         }
//     } catch (error) {
//         console.error('Error refreshing access token:', error);
//     }
// }




// Utility to fetch tokens from cookies
// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
//     return null;
//   }
  
