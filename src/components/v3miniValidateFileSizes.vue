<template>
    <div>
        <div v-if="analysis && false">
            <div v-for="(value, key) in analysis.groupResults" :key="key">
                <div class="red--text">IN PROGRESS</div>
                {{key}}
                <div v-for="(subvalue, subkey) in value" :key="subkey">
                    <div>{{subkey}}: {{subvalue}}</div>

                </div>
                <!-- <div>
                    Sufficient Training Data Size: {{analysis.groupResults.combined.testing_size_valid}}
                </div>
                <div>
                    Sufficient Testing Data Size: {{analysis.groupResults.combined.testing_size_valid}}
                </div>
                <div>
                    Sufficient Total Data Size: {{analysis.groupResults.combined.total_size_valid}}
                </div>   
                <div>
                    rows_max_valid: {{analysis.groupResults.combined.rows_max_valid}}
                </div>   
                <div>
                    cols_max_valid: {{analysis.groupResults.combined.cols_max_valid}}
                </div>                                                
                 -->
                
            </div>

        </div>
        <div v-else>
            ...adding additional checks...

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