<template>
    <div class="inline-div">
        <v-chip small v-if="type == 'train'" :color="mxfileTypeColor(type)" dark>Training</v-chip>
        <v-chip small v-if="type == 'test'" :color="mxfileTypeColor(type)" dark>Testing</v-chip>
        <v-chip small v-if="type == 'combined'" :color="mxfileTypeColor(type)" dark>Combined</v-chip>
    </div>
</template>
<script>    
import v3Mixin from "@/components/v3Mixin.js";
export default {
    name: 'v3miniValidate',
    mixins: [ v3Mixin ],
    props: {
        type: {
            type: String,
            default: 'combined'
        },
    }
}
</script>
<style scoped>
.inline-div {
    display: inline;
}
</style>