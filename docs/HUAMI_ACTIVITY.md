# Experimental activity decoder

The candidate legacy realtime activity characteristic is 00000007-0000-3512-2118-0009af100700. The experimental decoder assumes one leading byte and three unsigned little-endian 32-bit fields (steps, distance in metres, calories). This layout is a hypothesis pending verification against pinned Gadgetbridge source and device captures; the synthetic tests verify only the assumed layout. Do not enable this decoder in a runtime session until verified. Other packet lengths are rejected. Battery and historical activity formats require separate verification.
