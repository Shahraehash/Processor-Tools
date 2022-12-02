<template>
    <div>
        <div v-if="analysis">
            
            <v-row>
                <v-col cols="6">
                    <v-card outlined>

                    </v-card>
                </v-col>
            </v-row>

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