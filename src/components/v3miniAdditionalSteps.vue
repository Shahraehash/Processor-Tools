<template>
    <div class="text-center">
        <div class="text-h6 primary--text">Additional Steps</div>
          <v-row justify="center">
            <v-col cols="4" v-for="(item, key) in optionalComponents" :key="key">
              <v-card outlined @click="$emit('addComponent', item.component)" :disabled="item.disabled" class="pa-3">
                <div class="overline">{{item.title}}</div>
                <v-icon x-large :color="item.icon == 'mdi-export' ? 'primary' : ''">{{item.icon}}</v-icon>
              </v-card>          
            </v-col>
          </v-row>
    </div>
</template>
<script>    
export default {
    name: 'v3miniAdditionalSteps',
    props: {
        optionalComponents: {
            type: Array,
            default: () => []
        },
        // currentFiles: {
        //     type: Array,
        //     default: () => []
        // },
    },
    mounted() {

        //Scroll element into view when mounted
        window.scrollTo(0,document.body.scrollHeight);

    },
    methods: {

    }
}
</script>
<style scoped>

</style>