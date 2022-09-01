<template>
    <div class="con">
            <teamplate v-for="notification in notifications">
                <div class="block">
                <div class="imgbx">
                    <img src="https://inews.gtimg.com/newsapp_bt/0/14511251306/1000" class="cover">
                </div>
                <div class="details" >
                    <ion-icon @click="$emit('deleteNotification', notification.username)" class="close" name="close"></ion-icon>
                    <div class="listHead">
                        <h4>{{ notification.username }}</h4>
                        <p class="time">{{ notification.time }}</p>
                    </div>
                    <div class="message_p" @click="$router.push({path: `/${notification.chat_id}`})">
                        <p>{{ notification.text }}</p>
                    </div>
                </div>
            </div>
            </teamplate>
    </div>
</template>

<script>
    export default {
        name: 'notification',
        props: ['notifications'],
    }
</script>

<style scoped>
.close {
    position: absolute;
    right: 0px
}

a {
    text-decoration: none;
}

.con {
    position: absolute;
    bottom: 0;
    right: 0;
    margin-right: 10px;
    margin-bottom: 10px;
    width: 20%;
}

.block {
    position: relative;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    cursor: pointer;
    background: #2d3044;
}

.block.active {
    background: #ebebeb;
}

.block:hover {
    background: #3c3f54;
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
    color: #fff;
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