<template>
    <div class="container">
        <sidebar
        v-if="!search"
        @search-change="changeSearch"
        @newMessage="getNotification"
        />
        <SearchSideBar 
        v-if="search"
        :searchText="searchText"
        @searchSidebar="searchSidebar"
        :info="info"
        :search_chats="search_chats"
        />
        <div class="right-side">
            <h4>Сhoose a chat room</h4>
        </div>
        <notification
        :notifications="notifications"
        @deleteNotification="deleteNotification"
        />
    </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'
import SearchSideBar from '@/components/SearchSideBar.vue'
import Notification from '@/components/Notification.vue'
import axios from 'axios'
export default {
    components: {
        Sidebar,
        SearchSideBar,
        Notification
    },
    data() {
        return {
            search: false,
            searchText: '',
            info: [],
            notifications: [],
            search_chats: []
        }
    },
    methods: {
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
        getNotification(data) {
            this.notifications.push(data)
        },
        async searchInfo() {
            const response = await axios.get(`user/?search=${this.searchText}`)
            const res_chats = await axios.get(`chats/?search=${this.searchText}`)
            this.info = response.data
            this.search_chats = res_chats.data
        },
        deleteNotification(username) {
            for (let notification of this.notifications) {
                if (notification.username == username) {
                    this.notifications.pop(notification)
                }
            }
        }
    },
    watch: {
        'searchText': {
            handler: 'searchInfo',
        },
    }
}
</script>

<style scoped>
.right-side h4 {
    display: flex;
    justify-content: center;
    margin-top: 30%;
}

</style>