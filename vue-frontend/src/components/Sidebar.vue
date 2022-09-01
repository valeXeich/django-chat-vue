<template>
    <div class="left-side">
        <!-- header -->
        <div class="header">
            <div class="userimg">
                <img src="https://inews.gtimg.com/newsapp_bt/0/14511251306/1000" class="cover">
            </div>
            <ul class="nav_icons">
                <li><ion-icon name="scan-circle-outline"></ion-icon></li>
                <li><ion-icon name="chatbox"></ion-icon></li>
                <li><ion-icon name="ellipsis-vertical"></ion-icon></li>
            </ul>
        </div>
        <!-- search -->
        <div class="search_chat">
            <div>
                <input @input="$emit('search-change', $event.target.value)" type="text" placeholder="Search or start new chat">
                <ion-icon name="search-outline"></ion-icon>
            </div>
        </div>
        <!-- chat -->
        <div class="chatlist">
            <card
            :chats="chats"
            />
        </div>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex';
    import Card from '@/components/Card.vue'
    import axios from 'axios';
    export default {
        emits: ['search-change', 'newMessage'],
        name: 'sidebar',
        computed: mapGetters(['token', 'username']),
        components: {
            Card
        },
        data() {
            return {
                chats: [],
                chatsSocket: ''
            }
        },
        methods: {
            async getChats() {
                const response = await axios.get('chats/')
                this.chats = response.data
            },
            connect() {
                this.chatsSocket = new WebSocket('ws:' + `127.0.0.1:8000/ws/chats/` + `?token=${this.token}`)
                this.chatsSocket.onopen = () => {
                    this.chatsSocket.onmessage = ({data}) => {
                        let data_message = JSON.parse(data)
                        this.updateMessage(data_message)
                        this.$emit('newMessage', data_message)
                    }
                }
            },
            updateMessage(data) {
                for (let chat of this.chats) {
                    if (data.chat_id == chat.id) {
                        chat.last_message = data.text;
                        chat.time = data.time;
                    }
                }
            }
        },
        mounted() {
            this.getChats()
        },
        created() {
            this.connect()
        },
        
    }
</script>

<style scoped>
.chatlist {
    position: relative;
    height: calc(100% - 110px);
    overflow-y: auto;
}

.left-side {
    position: relative;
    flex: 30%;
    background: #fff;
    border-right: 1px solid rgba(0, 0, 0, 0.2);
}

.search_chat {
    position: relative;
    width: 100%;
    height: 50px;
    background: #f6f6f6;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 15px;
}

.search_chat div {
    width: 100%;
}

.search_chat div input {
    width: 100%;
    outline: none;
    border: none;
    background: #fff;
    padding: 6px;
    height: 38px;
    border-radius: 30px;
    font-size: 14px;
    padding-left: 40px;
}

.search_chat div input::placeholder {
    color: #bbb;
}

.search_chat div ion-icon {
    position: absolute;
    left: 30px;
    top: 14px;
    font-size: 1.2em;
}
</style>