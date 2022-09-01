import { createStore } from 'vuex'

export default createStore({
  state: {
    token: "",
    isAuthenticated: false,
    username: '',
    isFromSearch: false
  },
  getters: {
    isAuthenticated(state) {
      return state.isAuthenticated;
    },
    username(state) {
      return state.username;
    },
    token(state) {
      return state.token
    },
    isFromSearch(state) {
      return state.isFromSearch
    }
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem("auth_token")) {
        state.token = localStorage.getItem("auth_token");
        state.isAuthenticated = true;
        state.username = localStorage.getItem("username");
      } else {
        state.token = "";
        state.isAuthenticated = false;
        state.username = '';
      }
    },
  },
  actions: {
  },
  modules: {
  }
})
