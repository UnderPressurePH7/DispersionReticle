package com.dispersionreticle.reduction
{
    import flash.display.Sprite;
    import flash.display.Shape;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFieldAutoSize;

    public class ReductionPanelOld extends Sprite
    {
        private var _hitShape:Shape;
        private var _trackShape:Shape;
        private var _ticksShape:Shape;
        private var _sliderShape:Shape;
        private var _percentText:TextField;
        private var _statusText:TextField;

        private var _trackHeight:Number = 120;
        private var _tickCount:int = 20;
        private var _tickWidthSmall:Number = 5;
        private var _tickWidthMain:Number = 8;

        private static const HIT_PADDING_X:Number = 30;
        private static const HIT_PADDING_TOP:Number = 30;
        private static const HIT_PADDING_BOTTOM:Number = 30;

        private static const COLOR_RED:uint = 0xCC0000;
        private static const COLOR_YELLOW:uint = 0xCCCC00;
        private static const COLOR_GREEN:uint = 0x00CC00;

        public function ReductionPanelOld()
        {
            super();

            _hitShape = new Shape();
            _hitShape.graphics.beginFill(0x000000, 0);
            _hitShape.graphics.drawRect(
                -HIT_PADDING_X,
                -HIT_PADDING_TOP,
                HIT_PADDING_X * 2 + _tickWidthMain + 4,
                _trackHeight + HIT_PADDING_TOP + HIT_PADDING_BOTTOM
            );
            _hitShape.graphics.endFill();
            addChild(_hitShape);

            _trackShape = new Shape();
            addChild(_trackShape);

            _ticksShape = new Shape();
            addChild(_ticksShape);

            _sliderShape = new Shape();
            addChild(_sliderShape);

            var textFormat:TextFormat = new TextFormat();
            textFormat.font = "$FieldFont";
            textFormat.size = 13;
            textFormat.bold = true;

            _statusText = new TextField();
            _statusText.defaultTextFormat = textFormat;
            _statusText.autoSize = TextFieldAutoSize.CENTER;
            _statusText.selectable = false;
            _statusText.mouseEnabled = false;
            addChild(_statusText);

            _percentText = new TextField();
            _percentText.defaultTextFormat = textFormat;
            _percentText.autoSize = TextFieldAutoSize.CENTER;
            _percentText.selectable = false;
            _percentText.mouseEnabled = false;
            addChild(_percentText);

            _drawTrackAndTicks();
        }

        private function _drawTrackAndTicks():void
        {
            // Thin vertical track line
            _trackShape.graphics.clear();
            _trackShape.graphics.lineStyle(2, 0xCCCCCC, 0.7);
            _trackShape.graphics.moveTo(0, 0);
            _trackShape.graphics.lineTo(0, _trackHeight);

            // Horizontal ticks to the RIGHT of the track
            _ticksShape.graphics.clear();
            var tickSpacing:Number = _trackHeight / _tickCount;

            for (var i:int = 0; i <= _tickCount; i++)
            {
                var y:Number = _trackHeight - (i * tickSpacing);
                var isMain:Boolean = (i % 5 == 0);
                var tw:Number = isMain ? _tickWidthMain : _tickWidthSmall;
                var thickness:Number = isMain ? 2 : 1;

                _ticksShape.graphics.lineStyle(thickness, 0xCCCCCC, isMain ? 0.8 : 0.5);
                _ticksShape.graphics.moveTo(2, y);
                _ticksShape.graphics.lineTo(2 + tw, y);
            }
        }

        public function setData(aimingPercent:Number, timeLabel:String, percentLabel:String, aimedLabel:String):void
        {
            var clampedPercent:Number = Math.max(0, Math.min(100, aimingPercent));
            var color:uint = _getColorForPercent(clampedPercent);

            // Slider indicator - horizontal line at current position
            var sliderY:Number = _trackHeight - (_trackHeight * clampedPercent / 100.0);

            _sliderShape.graphics.clear();
            _sliderShape.graphics.lineStyle(3, color, _getSliderAlpha(clampedPercent));
            _sliderShape.graphics.moveTo(-4, sliderY);
            _sliderShape.graphics.lineTo(2 + _tickWidthMain, sliderY);

            // Status text above
            if (clampedPercent >= 99.5)
            {
                _statusText.textColor = COLOR_GREEN;
                _statusText.text = aimedLabel;
            }
            else
            {
                _statusText.textColor = color;
                _statusText.text = timeLabel;
            }
            _statusText.x = -(_statusText.textWidth / 2);
            _statusText.y = -22;

            // Percent text below
            _percentText.textColor = color;
            _percentText.text = percentLabel;
            _percentText.x = -(_percentText.textWidth / 2);
            _percentText.y = _trackHeight + 4;
        }

        private function _getSliderAlpha(aimingPercent:Number):Number
        {
            if (aimingPercent >= 100.0) return 0.6;
            if (aimingPercent < 80.0) return 1.0;
            return 1.0 - 0.4 * ((aimingPercent - 80.0) / 20.0);
        }

        private function _getColorForPercent(percent:Number):uint
        {
            if (percent < 50.0) return COLOR_RED;
            if (percent < 85.0) return COLOR_YELLOW;
            return COLOR_GREEN;
        }

        public function get panelWidth():Number { return _tickWidthMain + 10; }
        public function get panelHeight():Number { return _trackHeight + 40; }
    }
}
