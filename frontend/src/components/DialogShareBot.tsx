import React, { useCallback, useMemo, useState } from 'react';
import { BaseProps } from '../@types/common';
import Button from './Button';
import ModalDialog from './ModalDialog';
import { Trans, useTranslation } from 'react-i18next';
import { BotMeta } from '../@types/bot';
import Toggle from './Toggle';
import copy from 'copy-to-clipboard';

type Props = BaseProps & {
  isOpen: boolean;
  target?: BotMeta;
  onToggleShare: (botId: string) => void;
  onClose: () => void;
};

const DialogShareBot: React.FC<Props> = (props) => {
  const { t } = useTranslation();

  const [labelCopy, setLabelCopy] = useState(t('bot.button.copy'));

  const isShared = useMemo(() => {
    return props.target?.isPublic ?? false;
  }, [props.target?.isPublic]);

  const url = useMemo(() => {
    return `${window.location.origin}/bot/${props.target?.id}`;
  }, [props.target]);

  const onClickCopy = useCallback(() => {
    copy(url);
    setLabelCopy(t('bot.button.copied'));

    setTimeout(() => {
      setLabelCopy(t('bot.button.copy'));
    }, 3000);
  }, [t, url]);

  return (
    <ModalDialog {...props} title={t('bot.shareDialog.title')}>
      <div className="flex">
        <Trans
          i18nKey={
            isShared
              ? 'bot.shareDialog.on.content'
              : 'bot.shareDialog.off.content'
          }
          values={{
            title: props.target?.title,
          }}
          components={{
            Bold: <span className="font-bold" />,
          }}
        />

        <Toggle
          value={props.target?.isPublic ?? false}
          onChange={() => {
            props.onToggleShare(props.target?.id ?? '');
          }}
        />
      </div>

      {isShared && (
        <div className="mt-3 flex justify-between rounded border border-aws-squid-ink/50 bg-aws-paper">
          <input
            type="text"
            className="my-2 ml-2 w-full bg-aws-paper"
            readOnly
            value={url}
          />
          <Button
            outlined
            className="rounded-none rounded-r border-0 border-l bg-white"
            onClick={onClickCopy}>
            {labelCopy}
          </Button>
        </div>
      )}

      <div className="mt-6 flex justify-end gap-2">
        <Button onClick={props.onClose} className="p-2">
          {t('button.done')}
        </Button>
      </div>
    </ModalDialog>
  );
};

export default DialogShareBot;
