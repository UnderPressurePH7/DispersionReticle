package com.dispersionreticle.reduction
{
    import flash.display.Sprite;
    import flash.display.Shape;
    import flash.filters.GlowFilter;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFormatAlign;

    public class ReductionPanelNew extends Sprite
    {
        private var _hitShape:Shape;
        private var _barShape:Shape;
        private var _percentText:TextField;
        private var _statusText:TextField;

        private static const BAR_WIDTH:Number = 13;
        private static const BAR_HEIGHT:Number = 90;
        private static const SEGMENT_COUNT:int = 28;
        private static const SEGMENT_GAP:Number = 1;

        private static const LABEL_WIDTH:Number = 90;
        private static const STATUS_FONT_SIZE:int = 18;
        private static const PERCENT_FONT_SIZE:int = 16;

        private static const HIT_PADDING_X:Number = 36;
        private static const HIT_PADDING_TOP:Number = 32;
        private static const HIT_PADDING_BOTTOM:Number = 28;

        private static const COLOR_RED:uint = 0xFF1414;
        private static const COLOR_YELLOW:uint = 0xFFD51A;
        private static const COLOR_GREEN:uint = 0xA8FF2A;
        private static const COLOR_EMPTY:uint = 0x050505;

        public function ReductionPanelNew()
        {
            super();

            _hitShape = new Shape();
            _hitShape.graphics.beginFill(0x000000, 0);
            _hitShape.graphics.drawRect(
                -HIT_PADDING_X,
                -HIT_PADDING_TOP,
                BAR_WIDTH + HIT_PADDING_X * 2,
                BAR_HEIGHT + HIT_PADDING_TOP + HIT_PADDING_BOTTOM
            );
            _hitShape.graphics.endFill();
            addChild(_hitShape);

            _barShape = new Shape();
            addChild(_barShape);

            _statusText = _createLabel(STATUS_FONT_SIZE);
            _statusText.y = -28;
            addChild(_statusText);

            _percentText = _createLabel(PERCENT_FONT_SIZE);
            _percentText.y = BAR_HEIGHT + 2;
            addChild(_percentText);
        }

        public function setData(aimingPercent:Number, timeLabel:String, percentLabel:String, aimedLabel:String):void
        {
            var clampedPercent:Number = Math.max(0, Math.min(100, aimingPercent));
            var barColor:uint = _getColorForPercent(clampedPercent);
            var filledSegments:int = int(Math.round((SEGMENT_COUNT * clampedPercent) / 100.0));
            if (clampedPercent <= 0)
            {
                filledSegments = 0;
            }
            if (filledSegments > SEGMENT_COUNT)
            {
                filledSegments = SEGMENT_COUNT;
            }

            _drawSegmentedBar(filledSegments, barColor);

            if (clampedPercent >= 99.5)
            {
                _setLabel(_statusText, aimedLabel, COLOR_GREEN);
            }
            else
            {
                _setLabel(_statusText, timeLabel, barColor);
            }

            _setLabel(_percentText, percentLabel, barColor);
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
            label.x = (BAR_WIDTH - LABEL_WIDTH) / 2;
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

        private function _drawSegmentedBar(filledSegments:int, color:uint):void
        {
            _barShape.graphics.clear();

            var segmentStep:Number = BAR_HEIGHT / SEGMENT_COUNT;
            var segmentHeight:Number = Math.max(1.0, segmentStep - SEGMENT_GAP);
            var highlight:uint = _mixColor(color, 0xFFFFFF, 0.45);
            var shade:uint = _mixColor(color, 0x000000, 0.28);
            var y:Number;

            for (var i:int = 0; i < SEGMENT_COUNT; i++)
            {
                y = BAR_HEIGHT - ((i + 1) * segmentStep) + SEGMENT_GAP * 0.5;

                if (i >= filledSegments)
                {
                    _barShape.graphics.beginFill(COLOR_EMPTY, 0.25);
                    _barShape.graphics.drawRect(1, y + 1, BAR_WIDTH - 2, segmentHeight);
                    _barShape.graphics.endFill();
                    continue;
                }

                _barShape.graphics.beginFill(0x000000, 0.85);
                _barShape.graphics.drawRect(-1, y - 1, BAR_WIDTH + 2, segmentHeight + 2);
                _barShape.graphics.endFill();

                _barShape.graphics.beginFill(color, 0.98);
                _barShape.graphics.drawRect(0, y, BAR_WIDTH, segmentHeight);
                _barShape.graphics.endFill();

                _barShape.graphics.beginFill(highlight, 0.85);
                _barShape.graphics.drawRect(1, y + 1, 2, Math.max(1, segmentHeight - 2));
                _barShape.graphics.endFill();

                _barShape.graphics.beginFill(shade, 0.55);
                _barShape.graphics.drawRect(BAR_WIDTH - 3, y + 1, 2, Math.max(1, segmentHeight - 2));
                _barShape.graphics.endFill();
            }

            _barShape.graphics.lineStyle(1, 0x000000, 0.55);
            _barShape.graphics.drawRect(-1, -1, BAR_WIDTH + 2, BAR_HEIGHT + 2);
        }

        private function _getColorForPercent(percent:Number):uint
        {
            if (percent < 50.0) return COLOR_RED;
            if (percent < 85.0) return COLOR_YELLOW;
            return COLOR_GREEN;
        }

        private function _mixColor(color:uint, target:uint, ratio:Number):uint
        {
            var sourceRatio:Number = 1.0 - ratio;
            var r:int = int((((color >> 16) & 0xFF) * sourceRatio) + (((target >> 16) & 0xFF) * ratio));
            var g:int = int((((color >> 8) & 0xFF) * sourceRatio) + (((target >> 8) & 0xFF) * ratio));
            var b:int = int(((color & 0xFF) * sourceRatio) + ((target & 0xFF) * ratio));
            return uint((r << 16) | (g << 8) | b);
        }

        public function get panelWidth():Number { return BAR_WIDTH; }
        public function get panelHeight():Number { return BAR_HEIGHT + 40; }
    }
}
