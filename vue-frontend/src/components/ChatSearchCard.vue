<template>
    <template v-for="chat in info" :key="chat.id">
    <div class="block unread" @click="toChat(chat.id)">
                <div class="imgbx">
                    <img src="https://inews.gtimg.com/newsapp_bt/0/14511251306/1000" class="cover">
                </div>
                <div class="details">
                        <div class="listHead">
                            <h4>{{ chat.companion }}</h4>
                        </div>
                        <div class="message_p">
                            <p>{{ chat.last_message }}</p>
                            <b v-if="chat.unreaded_messages > 0">{{ chat.unreaded_messages }}</b>
                        </div>
                </div>
            </div>
            </template>
</template>

<script>
    export default {
        name: 'chat-search',
        props: ['info'],
        methods: {
            toChat(id) {
                this.$router.push({path: `/${id}`})
            }
        }
    }
</script>

<style scoped>
.block {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    cursor: pointer;
}

.block.active {
    background: #ebebeb;
}

.block:hover {
    background: #f5f5f5;
}

.block .imgbx {
    position: relative;
    height: 45px;
    min-width: 45px;
    overflow: hidden;
    border-radius: 50%;
    margin-right: 10px;
}

.block .details {
    position: relative;
    width: 100%;
}

.block .details .listHead {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: -30px;
}

.block .details .listHead h4 {
    font-size: 1.1em;
    font-weight: 600;
    color: #111;
}

.block .details .listHead .time {
    font-size: 0.75em;
    color: #aaa;
}

.block .details .listHead .time {
    color: #111;
}

.block.unread .details .listHead .time {
    color: #06d755
}

.message_p {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.message_p p {
    color: #aaa;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    font-size: 0.9em;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}

.message_p b {
    background: #06d755;
    color: #fff;
    min-width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 0.75em;
}

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
</style>