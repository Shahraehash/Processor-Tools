<template>
    <div>
        <div>
            {{original.files.length}} file<span v-if="original.files.length != 1">s</span>
            →
            {{final.files.length}} file<span v-if="final.files.length != 1">s</span>
        </div>
        <div>
            Rows missing data: {{original.missing}} → {{final.missing}}
        </div>        
        <div>
            Total Rows: {{original.rows}} → {{final.rows}}

        </div>
        <div>
            Total Columns: {{original.cols}} → {{final.cols}}
        </div>
        <div>
            Added Columns: 
            <v-chip class="mx-1" small color="primary" dark v-for="col, colKey in columnDiff.added" :key="colKey">{{col}}</v-chip>
        </div>        
        <div>
            Removed Columns: 
            <v-chip class="mx-1" small color="red" dark v-for="col, colKey in columnDiff.removed" :key="colKey">{{col}}</v-chip>
        </div>            
    </div>
</template>
<script>    
import underscore from 'underscore'

export default {
    name: 'v3miniFileInfo',
    props: {
        originalArray: {
            type: Array,
            default: () => [],
            deep: true
        },
        finalArray: {
            type: Array,
            default: () => [],
            deep: true
        },        
    },
    computed: {
        original() {
            return this.mapProcess(this.originalArray)
        },
        final() {
            return this.mapProcess(this.finalArray)
        },
        columnDiff() {

            return {
                removed: underscore.difference(this.original.columnList, this.final.columnList),
                added: underscore.difference(this.final.columnList, this.original.columnList)
            }

        }
    },
    methods: {
        mapProcess(arr) {
            let rows = 0
            let missing = 0
            let files = []
            arr.map((item) => {
                files.push(item.name)
                rows += item.size.rows
                missing += item.missing.rows
            })
            let columnList = arr[0].names.cols
            let cols = columnList.length

            return {
                files,
                rows,
                missing,
                cols,
                columnList
            }
        }

    }
}
</script>
<style scoped>
.inline-div {
    display: inline;
}
</style>