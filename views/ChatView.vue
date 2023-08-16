<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 rounded-lg">
              <div class="space-y-4">
                <div 
                    class="flex items-center justify-between"
                    v-for="chat in chats"
                    v-bind:key="chat.id"
                >
                    <div class="flex items-center space-x-2">
                        <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                        <p class="text-xs font-bold">{{ chat.user.name }}</p>
                    </div>

                    <span class="text-xs text-gray-500">{{ chat.modified_at_formatted }}</span>
                </div>


              </div>
            </div>
        </div>

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="flex flex-col flex-grow p-4">
                    <template
                        v-for="message in chatHistory" :key="message.id"
                    >
                        <div 
                            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                            v-if="message.type === 'user'"
                        >
                            <div>
                                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p class="text-sm">You: {{ message.text }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            </div>
                        </div>

                        <div v-if="loading" class="bg-white border border-gray-200 rounded-lg p-4">
                            <div class="flex justify-center items-center h-32">
                                <svg class="animate-spin h-5 w-5 text-gray-600 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647zM12 20a8 8 0 110-16 8 8 0 010 16z"></path>
                                </svg>
                                <p class="text-gray-600">Processing...</p>
                            </div>
                        </div>

                        <div 
                            class="flex w-full mt-2 space-x-3 max-w-md"
                            v-else-if="message.type === 'chatbot'"
                        >
                            <div>
                                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="text-sm" v-html="formatMessageText(message.text)"></p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                            </div>
                        </div>

                    </template>

                    
                </div>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg">
               <form v-on:submit.prevent="sendMessage">
                    <div class="p-4">
                        <textarea v-model="userInput" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What enquiry do you have for the chatbot?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Send</button>
                    </div>
                </form>
           </div>
        </div>
    </div>
  
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            chatHistory: [],
            userInput: '',
            loading: false,
            chats: [],
            activeChats: {}
        }
    },

    mounted() {
        this.getChats()
    },

    methods: {
        getChats() {
            console.log('getChats')

            axios
                .get('/api/chatbot/chat_list/')
                .then(response => {
                    console.log(response.data)

                    this.chats = response.data

                    if (this.chats.length) {
                        this.activeChats = this.chats[0]
                    }
                    this.getChatMessages()
                })
                .catch(error => {
                    console.log(error)
                })
        },

        getChatMessages() {
            console.log('getMessages')

            axios
                .get(`api/chatbot/chat_detail/${this.activeChats.id}/`)
                .then(response => {
                    console.log(response.data)

                    this.activeChats = response.data
                })
                .catch(error => {
                    console.log(error)
                })

        },


        formatMessageText(text) {
            // Replace newlines with HTML line breaks to preserve the formatting
            return text.replace(/\n/g, "<br>");
        },
        
        sendMessage() {
            this.chatHistory.push({id: Date.now(), type: 'user', text: this.userInput});
            this.loading = true; // set loading to true when sending the message

            axios
                .post('/api/chatbot/', { 'userInput': this.userInput })
                .then(response => {
                    console.log('data', response.data)
                    const chatBotResponse = response.data.response;
                    console.log('chatBotResponse', chatBotResponse)
                    this.chatHistory.push({id: Date.now(), type: 'chatbot', text: chatBotResponse });
                    console.log('ChatHistory', this.chatHistory)
                })
                .catch(error => {
                    console.log('error', error);
                })
                .finally(() => {
                    this.loading = false; // set loading to false when response is received
                })
        
            this.userInput = '';
        }



    }

}
</script>

<style>

</style>