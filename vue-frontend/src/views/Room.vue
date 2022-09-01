<template>
    <div class="container">

        <sidebar
        v-if="!search"
        @search-change="changeSearch"
        />
        <SearchSideBar 
        v-if="search"
        :searchText="searchText"
        @searchSidebar="searchSidebar"
        :info="info"
        :search_chats="search_chats"
        />

        <div class="right-side">
            <div class="header">
                <div class="imgText">
                    <div class="userimg">
                        <img src="https://inews.gtimg.com/newsapp_bt/0/14511251306/1000" class="cover">
                    </div>
                    <h4>{{ companion }}<br>
                        <span v-if="online_users.length > 1">onlile</span>
                        <span v-else="online_users.length > 1">offline</span>
                    </h4>
                </div>
                <ul class="nav_icons">
                    <li>
                        <ion-icon name="search-outline"></ion-icon>
                    </li>
                    <li>
                        <ion-icon name="ellipsis-vertical"></ion-icon>
                    </li>
                </ul>
            </div>
            <!-- chatbox -->
            <div class="chatBox">
                <template v-for="dialog in dialogs.messages">
                    <div v-if="dialog.sender == username" class="message my_message">
                        <p>{{ dialog.text }}<br>
                            <span>
                                {{ getTime(dialog.created) }}
                                <ion-icon v-if="dialog.readed || this.online_users.length == 2" name="checkmark-done"></ion-icon>
                                <ion-icon v-else name="checkmark"></ion-icon>
                            </span>
                        </p>
                    </div>
                    <div v-else class="message frnd_message">
                        <p>{{ dialog.text }}<br>
                            <span>
                                {{ dialog.created }} 
                                <ion-icon v-if="dialog.readed || this.online_users.length == 2" name="checkmark-done"></ion-icon>
                                <ion-icon v-else name="checkmark"></ion-icon>
                            </span>
                        </p>
                    </div>
                </template>
            </div>
            <!-- chat input -->
            <div class="chatbox_input">
                <ion-icon name="happy-outline"></ion-icon>
                <ion-icon name="attach-outline"></ion-icon>
                <input @keyup.enter="sendMessage" v-model="text" type="text" placeholder="Type a message">
                <ion-icon name="mic"></ion-icon>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Sidebar from '@/components/Sidebar.vue'
import SearchSideBar from '@/components/SearchSideBar.vue'
import axios from 'axios'
export default {
    components: {
        Sidebar,
        SearchSideBar
    },
    data() {
        return {
            status: 'disconnect',
            chatSocket: '',
            text: '',
            dialogs: [],
            chat_id: '',
            online_users: [],
            companion: '',
            search: false,
            searchText: '',
            info: [],
            search_chats: []
        }
    },
    created() {
        this.connect()
    },
    methods: {
        getTime(time) {
            if (time == undefined) {
                return `${new Date().getHours()}:${new Date().getMinutes()}`
            } else {
                return time
            }
        },
        connect() {
            if (this.isFromSearch) {
                let random_number = Math.floor(Math.random() * (100*100 - 100*50 + 1)) + 100*50
                this.chatSocket = new WebSocket('ws:' + `127.0.0.1:8000/ws/chat/` + random_number + `/?token=${this.token}`);
            } else {
                this.chatSocket = new WebSocket('ws:' + `127.0.0.1:8000/ws/chat/` + this.$route.params.id + `/?token=${this.token}`);
            }
            this.chatSocket.onopen = () => {
            this.chatSocket.send(JSON.stringify({
                'type': 'user_connect',
                'username': this.username,
                'message': 'connected'
            }))
                this.chatSocket.onmessage = ({data}) => {
                    this.chat_id = JSON.parse(data).chat_id
                    if (this.isFromSearch && this.chat_id) {
                    this.$store.state.isFromSearch = false
                    this.$router.push({path: `/${this.chat_id}`})
                }
                    if (!JSON.parse(data).online) {
                        this.dialogs.messages.push(JSON.parse(data))
                    } else {
                        this.online_users = JSON.parse(data).online
                    }
                }
            }
        },
        changeSearch(data) {
            if (data.length) {
                this.searchText = data
                this.search = true
            } else {
                this.search = false
            }
        },
        searchSidebar(data) {
            if (!data.length) {
                this.search = false
            } else {
                this.searchText = data
            }
        },
        async searchInfo() {
            const response = await axios.get(`user/?search=${this.searchText}`)
            const res_chats = await axios.get(`chats/?search=${this.searchText}`)
            this.info = response.data
            this.search_chats = res_chats.data
        },
        sendMessage(e) {
            let companion_online = ''
                if (this.online_users.length == 2) {
                    let username = this.username
                    companion_online = this.online_users.filter(function(user) {return user !== username})
                }
            this.chatSocket.send(JSON.stringify({
                'type': 'chat_message',
                'message': this.text,
                'is_from_search': this.$store.state.isFromSearch,
                'companion_online': companion_online,
                'companion': this.companion
            }))
            this.text = ''
        },
        async getMessages() {
            if (!this.isFromSearch) {
                const response = await axios.get(`chat/${this.$route.params.id}/`)
                this.dialogs = response.data
                this.companion = response.data.companion
            } else {
                this.companion = this.$route.params.id
            }
        },
        disconnect() {
            this.chatSocket.send(JSON.stringify({
                'type': 'user_connect',
                'username': this.username,
                'message': 'disconnect'
            }))
            this.chatSocket.close();
            this.status = 'disconnect'
        },
    },
    computed: mapGetters(['username', 'token', 'isFromSearch']),
    mounted() {
        this.getMessages()
    },
    watch: {
        '$route': {
            handler: 'disconnect'
        },
        '$route.params.id': {
            handler: 'getMessages',
            immediate: true
        },
        'searchText': {
            handler: 'searchInfo',
        },
    }
}
</script>


<style scoped>
.imgText {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}

.imgText h4 {
    font-weight: 500;
    line-height: 1.2em;
    margin-left: 15px;
}

.imgText h4 span {
    font-size: 0.8em;
    color: #555
}

.chatBox {
    position: relative;
    width: 100%;
    height: calc(100% - 120px);
    padding: 50px;
    overflow-y: auto;
}

.message {
    position: relative;
    display: flex;
    width: 100%;
    margin: 5px 0;
}

.message p {
    position: relative;
    right: 0;
    text-align: right;
    max-width: 65%;
    padding: 12px;
    background: #dcf8c6;
    border-radius: 10px;
    font-size: 0.9em
}

.message p::before {
    content: '';
    position: absolute;
    top: 0px;
    right: -12px;
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #dcf8c6 0%, #dcf8c6 50%, transparent 50%, transparent);
}

.message p span {
    display: block;
    margin-top: 5px;
    font-size: 0.85em;
    opacity: 0.5;
}

.my_message {
    justify-content: flex-end;
}

.frnd_message {
    justify-content: flex-start;
}

.frnd_message p {
    background-color: #fff;
    text-align: left;
}

.message.frnd_message p::before {
    content: '';
    position: absolute;
    top: 0px;
    left: -12px;
    width: 20px;
    height: 20px;
    background: linear-gradient(225deg, #fff 0%, #fff 50%, transparent 50%, transparent);
}

.chatbox_input {
    position: relative;
    width: 100%;
    height: 60px;
    background: #f0f0f0;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chatbox_input ion-icon {
    cursor: pointer;
    font-size: 1.8em;
    color: #51585c;
}

.chatbox_input ion-icon:nth-child(1) {
    margin-right: 15px;
}

.chatbox_input input {
    position: relative;
    width: 90%;
    margin: 0 20px;
    padding: 10px 20px;
    border: none;
    outline: none;
    border-radius: 30px;
    font-size: 1em;
}
</style>