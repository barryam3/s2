import { Injectable } from '@angular/core';

import { filterInPlace } from '../utils';

export enum Context {
  Success= 'success',
  Info= 'info',
  Warning= 'warning',
  Danger= 'danger',
}

export interface Message {
  content: string;
  context: Context;
  id: number;
}

@Injectable()
export class MessageService {
  messages: Message[] = [];
  nextID = 0;

  add(content: string, context: Context= Context.Info) {
    this.messages.push({ content, context, id: this.nextID });
    this.nextID += 1;
  }

  clear() {
    this.messages = [];
    this.nextID = 0;
  }

  remove(message: Message) {
    filterInPlace(this.messages, m => m.id !== message.id);
  }
}
