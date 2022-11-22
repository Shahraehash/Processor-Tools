<template>
    <div>
        <div v-if="analysis">

            <v-row>
                <v-col cols="4">
                    <div class="overline">Row Numbers</div>
                        {TODO ADD}

                </v-col>
                <v-col cols="4">
                    <div class="overline">Column Numbers</div>
                        {TODO ADD}
                    
                </v-col>
                <v-col cols="4">
                    <div class="overline">Missing Data</div>
                        {TODO ADD}
                    
                </v-col>                                
            </v-row>

        </div>
        <div v-else>
            No data

        </div>
    </div>
</template>
<script>    
export default {
    name: 'v3miniValidate',
    props: {
        currentFiles: {
            type: Array,
            default: () => []
        },
        target: {
            type: String,
            default: null
        },
        analysis: {
            type: Object,
            default: null
        },
    }
}
</script>
<style scoped>

</style>