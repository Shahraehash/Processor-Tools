<template>
    <div>
        <div>
            <strong>{{fileInfo.name}}</strong>
        </div>            
        <div>
            Rows: {{fileInfo.size.rows}}
        </div>        
        <div>
            Cols: {{columns}}
            <!-- Requires correction d/t audit columns -->
        </div>           
        <div>
            Missing Rows: {{fileInfo.missing.rows}}
        </div>         
    </div>
</template>
<script>    

export default {
    name: 'v3miniFileInfo',
    props: {
        fileInfo: {
            type: Object,
            default: () => {}
        },
    },
    computed: {
        columns() {
            return this.fileInfo.names.cols.filter(x => !['origin_file_name','origin_file_source_row'].includes(x)).length
        }
    },
    methods: {

    }
}
</script>
<style scoped>
.inline-div {
    display: inline;
}
</style>