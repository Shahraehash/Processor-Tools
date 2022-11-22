<template>
    <div class="text-center">
        <div class="text-h6 primary--text">Additional Steps</div>
          <v-row justify="center">
            <v-col cols="4" v-for="(item, key) in filteredOptionalComponents" :key="key">
              <v-card outlined @click="$emit('addComponent', item.component)" class="pa-3">
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
        componentList: {
            type: Array,
            default: () => []
        },
    },
    mounted() {

        //Scroll element into view when mounted
        window.scrollTo(0,document.body.scrollHeight);

    },
    computed: {
      filteredOptionalComponents() {
        return this.optionalComponents.filter(item => !this.componentList.includes(item.component))
      }
    }

}
</script>
<style scoped>

</style>