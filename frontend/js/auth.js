const authenticaotr = (()=>{
    let auth0 = null;

    // const fetchAuthConfig = () => fetch("/auth_config.json");

    const configureClient = async () => {
        // const response = await fetchAuthConfig();
        // const config = await response.json();
      
        auth0 = await createAuth0Client({
          domain: "casting-agency-capstone.auth0.com",
          client_id: "o8j0f3DEN9v3URxAXn1o65vJorxZNLJ1"
        });
      };

    return {auth0, configureClient}
})()