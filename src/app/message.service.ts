import { Injectable } from '@angular/core';

import { filterInPlace } from '../utils';

export enum Context {
  Success,
  Info,
  Warning,
  Danger
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

  add(message: string, context: Context=Context.Info) {
    this.messages.push({content: message, context: context, id: this.nextID});
    this.nextID += 1;
    console.log(this.messages);
  }

  clear() {
    this.messages = [];
    this.nextID = 0;
  }

  remove(message: Message) {
    filterInPlace(this.messages, m => m.id !== message.id);
  }
}