//Function to render data of profile in the dashboard
export async function fetching_data(){
    try{
        const response = await fetch('http://localhost:8000/api/user_data/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if(response.ok){
            const data = await response.json();
            console.log(data[0].image);
            sleep(7000);
            const profile = document.getElementsByClassName('profile')[0];
            profile.innerHTML = `
           
            <div class="usr">
            <img src="images/avatar.png" alt="profile">
                <span class="username">${data[0].login}</span>
                <span class="rank">Rank</span>
            </div>
                    `;
                    return;
        }
        else{
            console.error('Failed to fetch data');
        }
    }
    catch(error){
        console.error('Error fetching data:', error);
    }
    // return data;
}