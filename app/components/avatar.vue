<template>
  <avataaars
    :clotheType="avatar.clotheType"
    :clotheColor="avatar.clotheColor"
    :hairColor="avatar.hairColor"
    :skinColor="avatar.skinColor"
    :topColor="avatar.topColor"
    :topType="avatar.topType"
    :isCircle="avatar.isCircle"
    :circleColor="avatar.circleColor"
    :accessoriesType="avatar.accessoriesType"
    :eyebrowType="avatar.eyebrowType"
    :eyeType="avatar.eyeType"
    :mouthType="avatar.mouthType"
    :facialHairColor="avatar.facialHairColor"
    :facialHairType="avatar.facialHairType"
    :graphicType="avatar.graphicType">
  </avataaars>
</template>

<script>
import Avataaars from 'vuejs-avataaars'

export default {
  components: {
    Avataaars
  },
  props: ['avatar']
}
</script>
