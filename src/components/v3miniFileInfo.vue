<template>
    <div>
        <div>
            <strong>{{fileInfo.name}}</strong>
        </div>            
        <div>
            Rows: {{fileInfo.size.rows}}
        </div>        
        <div>
            Cols: {{fileInfo.size.cols}}
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
    methods: {

    }
}
</script>
<style scoped>
.inline-div {
    display: inline;
}
</style>