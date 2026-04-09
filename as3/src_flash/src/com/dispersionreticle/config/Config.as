package com.dispersionreticle.config
{
    public class Config
    {
        public var circleEnabled:Boolean = true;
        public var circleColor:uint = 0xFFFF00;
        public var reductionEnabled:Boolean = true;
        public var reductionStyle:String = "new";

        public function Config()
        {
        }

        public function updateReductionConfig(enabled:Boolean, style:String):void
        {
            reductionEnabled = enabled;
            reductionStyle = style;
        }
    }
}
