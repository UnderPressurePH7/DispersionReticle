package com.dispersionreticle.reduction
{
    import flash.display.Sprite;
    import flash.display.Shape;
    import flash.filters.GlowFilter;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFormatAlign;

    public class ReductionPanelOld extends Sprite
    {
        private var _hitShape:Shape;
        private var _trackShape:Shape;
        private var _ticksShape:Shape;
        private var _sliderShape:Shape;
        private var _percentText:TextField;
        private var _statusText:TextField;

        private static const TRACK_HEIGHT:Number = 118;
        private static const TICK_COUNT:int = 24;
        private static const TICK_SMALL:Number = 7;
        private static const TICK_MEDIUM:Number = 11;
        private static const TICK_MAIN:Number = 17;

        private static const LABEL_WIDTH:Number = 90;
        private static const STATUS_FONT_SIZE:int = 18;
        private static const PERCENT_FONT_SIZE:int = 17;

        private static const HIT_PADDING_X:Number = 42;
        private static const HIT_PADDING_TOP:Number = 34;
        private static const HIT_PADDING_BOTTOM:Number = 30;

        private static const COLOR_TICK:uint = 0xE7DFC9;
        private static const COLOR_TICK_DIM:uint = 0xAFA894;
        private static const COLOR_YELLOW:uint = 0xFFD51A;
        private static const COLOR_GREEN:uint = 0x22FF44;

        public function ReductionPanelOld()
        {
            super();

            _hitShape = new Shape();
            _hitShape.graphics.beginFill(0x000000, 0);
            _hitShape.graphics.drawRect(
                -HIT_PADDING_X,
                -HIT_PADDING_TOP,
                HIT_PADDING_X * 2,
                TRACK_HEIGHT + HIT_PADDING_TOP + HIT_PADDING_BOTTOM
            );
            _hitShape.graphics.endFill();
            addChild(_hitShape);

            _trackShape = new Shape();
            addChild(_trackShape);

            _ticksShape = new Shape();
            addChild(_ticksShape);

            _sliderShape = new Shape();
            addChild(_sliderShape);

            _statusText = _createLabel(STATUS_FONT_SIZE);
            _statusText.y = -31;
            addChild(_statusText);

            _percentText = _createLabel(PERCENT_FONT_SIZE);
            _percentText.y = TRACK_HEIGHT + 3;
            addChild(_percentText);

            _drawTrackAndTicks();
        }

        private function _drawTrackAndTicks():void
        {
            _trackShape.graphics.clear();
            _trackShape.graphics.lineStyle(3, 0x000000, 0.55);
            _trackShape.graphics.moveTo(0, 0);
            _trackShape.graphics.lineTo(0, TRACK_HEIGHT);
            _trackShape.graphics.lineStyle(1, COLOR_TICK, 0.75);
            _trackShape.graphics.moveTo(0, 0);
            _trackShape.graphics.lineTo(0, TRACK_HEIGHT);

            _ticksShape.graphics.clear();
            var tickSpacing:Number = TRACK_HEIGHT / TICK_COUNT;

            for (var i:int = 0; i <= TICK_COUNT; i++)
            {
                var y:Number = TRACK_HEIGHT - (i * tickSpacing);
                var isMain:Boolean = (i % 6 == 0);
                var isMedium:Boolean = (!isMain && i % 3 == 0);
                var halfWidth:Number = isMain ? TICK_MAIN : (isMedium ? TICK_MEDIUM : TICK_SMALL);
                var thickness:Number = isMain ? 2 : 1;
                var alpha:Number = isMain ? 0.9 : (isMedium ? 0.72 : 0.48);
                var tickColor:uint = isMain ? COLOR_TICK : COLOR_TICK_DIM;

                _ticksShape.graphics.lineStyle(thickness + 1, 0x000000, 0.45);
                _ticksShape.graphics.moveTo(-halfWidth, y + 1);
                _ticksShape.graphics.lineTo(halfWidth, y + 1);

                _ticksShape.graphics.lineStyle(thickness, tickColor, alpha);
                _ticksShape.graphics.moveTo(-halfWidth, y);
                _ticksShape.graphics.lineTo(halfWidth, y);
            }
        }

        public function setData(aimingPercent:Number, timeLabel:String, percentLabel:String, aimedLabel:String):void
        {
            var clampedPercent:Number = Math.max(0, Math.min(100, aimingPercent));
            var sliderY:Number = TRACK_HEIGHT - (TRACK_HEIGHT * clampedPercent / 100.0);
            var sliderAlpha:Number = _getSliderAlpha(clampedPercent);

            _sliderShape.graphics.clear();
            _sliderShape.graphics.lineStyle(4, 0x000000, 0.65);
            _sliderShape.graphics.moveTo(-TICK_MAIN - 3, sliderY + 1);
            _sliderShape.graphics.lineTo(TICK_MAIN + 3, sliderY + 1);
            _sliderShape.graphics.lineStyle(2, COLOR_YELLOW, sliderAlpha);
            _sliderShape.graphics.moveTo(-TICK_MAIN - 2, sliderY);
            _sliderShape.graphics.lineTo(TICK_MAIN + 2, sliderY);

            if (clampedPercent >= 99.5)
            {
                _setLabel(_statusText, aimedLabel, COLOR_GREEN);
            }
            else
            {
                _setLabel(_statusText, timeLabel, COLOR_GREEN);
            }

            _setLabel(_percentText, percentLabel, COLOR_YELLOW);
        }

        private function _createLabel(size:int):TextField
        {
            var textFormat:TextFormat = new TextFormat();
            textFormat.font = "$FieldFont";
            textFormat.size = size;
            textFormat.bold = true;
            textFormat.align = TextFormatAlign.CENTER;

            var label:TextField = new TextField();
            label.defaultTextFormat = textFormat;
            label.width = LABEL_WIDTH;
            label.height = size + 8;
            label.x = -LABEL_WIDTH / 2;
            label.selectable = false;
            label.mouseEnabled = false;
            label.filters = [new GlowFilter(0x000000, 1.0, 2, 2, 8, 1)];
            return label;
        }

        private function _setLabel(label:TextField, text:String, color:uint):void
        {
            label.text = (text != null) ? text : "";
            label.textColor = color;
        }

        private function _getSliderAlpha(aimingPercent:Number):Number
        {
            if (aimingPercent >= 99.5) return 0.75;
            return 1.0;
        }

        public function get panelWidth():Number { return TICK_MAIN * 2; }
        public function get panelHeight():Number { return TRACK_HEIGHT + 42; }
    }
}
