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
                <input autofocus v-model="searchInput" @input="$emit('searchSidebar', $event.target.value)" type="text" placeholder="Search or start new chat">
                <ion-icon name="search-outline"></ion-icon>
            </div>
        </div>
        
        <!-- chat -->
        <div class="chatlist">
            <span class="topic">Глобальный поиск</span>
           <card-search
           :info="info"
           />
           <span class="topic">Чаты</span>
           <ChatSearchCard
            :info="search_chats"
           />
        </div>
        
    </div>
</template>

<script>
    import CardSearch from '@/components/CardSearch.vue'
    import ChatSearchCard from '@/components/ChatSearchCard.vue'
    export default {
        emits: ['searchSidebar'],
        name: 'sidebar-search',
        components: {
    CardSearch,
    ChatSearchCard,
},
        props: ['searchText', 'info', 'search_chats'],
        data() {
            return {
                searchInput: this.searchText
            }
        }
    }
</script>

<style scoped>

.topic {
    color: #aaa;
    font-size: 0.9em;
    padding-left: 15px;
    font-weight: bold;
}

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