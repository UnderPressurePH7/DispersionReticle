package com.dispersionreticle.reduction
{
    import flash.display.Sprite;
    import flash.display.Shape;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFieldAutoSize;

    public class ReductionPanelNew extends Sprite
    {
        private var _hitShape:Shape;
        private var _barShape:Shape;
        private var _ticksShape:Shape;
        private var _percentText:TextField;
        private var _statusText:TextField;

        private var _barWidth:Number = 14;
        private var _barHeight:Number = 100;
        private var _tickCount:int = 20;

        private static const HIT_PADDING_X:Number = 25;
        private static const HIT_PADDING_TOP:Number = 28;
        private static const HIT_PADDING_BOTTOM:Number = 28;

        private static const COLOR_RED:uint = 0xCC0000;
        private static const COLOR_YELLOW:uint = 0xCCCC00;
        private static const COLOR_GREEN:uint = 0x00CC00;

        public function ReductionPanelNew()
        {
            super();

            _hitShape = new Shape();
            _hitShape.graphics.beginFill(0x000000, 0);
            _hitShape.graphics.drawRect(
                -HIT_PADDING_X,
                -HIT_PADDING_TOP,
                _barWidth + HIT_PADDING_X * 2,
                _barHeight + HIT_PADDING_TOP + HIT_PADDING_BOTTOM
            );
            _hitShape.graphics.endFill();
            addChild(_hitShape);

            _barShape = new Shape();
            addChild(_barShape);

            _ticksShape = new Shape();
            addChild(_ticksShape);

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
        }

        public function setData(aimingPercent:Number, timeLabel:String, percentLabel:String, aimedLabel:String):void
        {
            var clampedPercent:Number = Math.max(0, Math.min(100, aimingPercent));
            var barColor:uint = _getColorForPercent(clampedPercent);
            var fillHeight:Number = (_barHeight * clampedPercent) / 100.0;

            // --- Draw bar ---
            _barShape.graphics.clear();

            // Background
            _barShape.graphics.beginFill(0x000000, 0.4);
            _barShape.graphics.drawRect(0, 0, _barWidth, _barHeight);
            _barShape.graphics.endFill();

            // Filled portion
            _barShape.graphics.beginFill(barColor, 0.8);
            _barShape.graphics.drawRect(0, _barHeight - fillHeight, _barWidth, fillHeight);
            _barShape.graphics.endFill();

            // Border
            _barShape.graphics.lineStyle(1, 0x333333, 0.6);
            _barShape.graphics.drawRect(0, 0, _barWidth, _barHeight);

            // --- Draw ticks ON TOP of bar ---
            _ticksShape.graphics.clear();
            var tickSpacing:Number = _barHeight / _tickCount;

            for (var i:int = 1; i < _tickCount; i++)
            {
                var y:Number = _barHeight - (i * tickSpacing);
                var isMain:Boolean = (i % 5 == 0);

                _ticksShape.graphics.lineStyle(isMain ? 2 : 1, 0x000000, isMain ? 0.7 : 0.4);
                _ticksShape.graphics.moveTo(0, y);
                _ticksShape.graphics.lineTo(_barWidth, y);
            }

            // --- Status text above bar ---
            if (clampedPercent >= 99.5)
            {
                _statusText.textColor = COLOR_GREEN;
                _statusText.text = aimedLabel;
            }
            else
            {
                _statusText.textColor = barColor;
                _statusText.text = timeLabel;
            }
            _statusText.x = (_barWidth / 2) - (_statusText.textWidth / 2);
            _statusText.y = -20;

            // --- Percent text below bar ---
            _percentText.textColor = barColor;
            _percentText.text = percentLabel;
            _percentText.x = (_barWidth / 2) - (_percentText.textWidth / 2);
            _percentText.y = _barHeight + 4;
        }

        private function _getColorForPercent(percent:Number):uint
        {
            if (percent < 50.0) return COLOR_RED;
            if (percent < 85.0) return COLOR_YELLOW;
            return COLOR_GREEN;
        }

        public function get panelWidth():Number { return _barWidth; }
        public function get panelHeight():Number { return _barHeight + 40; }
    }
}
