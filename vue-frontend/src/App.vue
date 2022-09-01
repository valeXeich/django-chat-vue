<template>
  <router-view/>
</template>

<script>
import axios from 'axios'
export default {
  mounted() {
    let recaptchaScript = document.createElement('script')
    let icons = document.createElement('script')
    recaptchaScript.setAttribute('src', 'https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js')
    recaptchaScript.setAttribute('type', 'module')
    icons.setAttribute('src', 'https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js')
    document.head.appendChild(recaptchaScript)
    document.head.appendChild(icons)
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  },
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Open-Sans:wght@300;400;500;600;700&display=swap');

* {
    margin: 0xp;
    padding: 0px;
    box-sizing: border-box;
    font-family: 'Open Sans', sans-serif;
}

body {
    margin: 0px;
    padding: 0px;
}

.cover {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.header {
    position: relative;
    width: 100%;
    height: 60px;
    background: #e5ddd5;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 15px;
}

.userimg {
    position: relative;
    width: 40px;
    height: 40px;
    overflow: hidden;
    border-radius: 50%;
    cursor: pointer;
}


.nav_icons {
    display: flex;
}

.nav_icons li {
    display: flex;
    list-style: none;
   cursor: pointer;
   color: #51585c;
   font-size: 1.5em;
   margin-left: 22px;
}

.container {
    position: relative;
    width: 100%;
    max-width: 100%;
    height: 100vh;
    background: #fff;
    box-shadow:0 1px 1px 0 rgba(0,0,0,0.06),0 2px 5px 0 rgba(0,0,0,0.06);
    display: flex;
}

.container .right-side {
    position: relative;
    flex: 70%;
    background: #e5ddd5;

}

.container .right-side::before {
   content: '';
   position: absolute;
   top: 0px;
   left: 0px;
   width: 100%;
   height: 100%;
   background: url('@/assets/images/pattern.png');
   opacity: 0.06;
}
</style>
