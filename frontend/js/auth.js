const authenticaotr = (() => {

  // The Auth0 client, initialized in configureClient()
  let auth0 = null;
  const targetUrl = "https://casting-agency-capstone.auth0.com/authorize?audience=executive&response_type=token&client_id=o8j0f3DEN9v3URxAXn1o65vJorxZNLJ1&redirect_uri=https://jlcruza.github.io/FSND-Capstone/frontend/"

  /**
* Starts the authentication flow
*/
  const login = async () => {
    try {
      console.log("Logging in", targetUrl);

      const options = {
        redirect_uri: window.location.origin
      };

      if (targetUrl) {
        options.appState = { targetUrl };
      }

      await auth0.loginWithRedirect(options);
    } catch (err) {
      console.log("Log in failed", err);
    }
  };


  /**
   * Executes the logout flow
   */
  const logout = () => {
    try {
      console.log("Logging out");
      auth0.logout({
        returnTo: window.location.origin
      });
    } catch (err) {
      console.log("Log out failed", err);
    }
  };


  /**
   * Checks to see if the user is authenticated. If so, `fn` is executed. Otherwise, the user
   * is prompted to log in
   * @param {*} fn The function to execute if the user is logged in
   */
  const requireAuth = async (fn) => {
    const isAuthenticated = await auth0.isAuthenticated();

    if (isAuthenticated) {
      return fn();
    }

    return login(targetUrl);
  };


  const configureClient = async () => {
    // const response = await fetchAuthConfig();
    // const config = await response.json();

    auth0 = await createAuth0Client({
      domain: "casting-agency-capstone.auth0.com",
      client_id: "o8j0f3DEN9v3URxAXn1o65vJorxZNLJ1"
    });
  };

  const getToken = () => {
    return auth0;
  }

  return { configureClient, getToken, login, logout, requireAuth }
})()